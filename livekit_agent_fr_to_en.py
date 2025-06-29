import logging
import os
from dotenv import load_dotenv

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    WorkerOptions,
    cli,
    RoomInputOptions,
    RoomOutputOptions,
    JobRequest,
    RoomIO,
)
from livekit.plugins import (
    openai,
    noise_cancellation,
)
from livekit.rtc import RemoteTrackPublication, RemoteParticipant

logger = logging.getLogger("bahasa-translator")
logger.setLevel(logging.INFO)

# Configuration
TARGET_PARTICIPANT = "ysf"  # Change this to target a different participant

load_dotenv()

class BahasaTranslator(Agent):
    def __init__(self) -> None:
        super().__init__(
             instructions=(
                "YOU ARE A PROFESSIONAL FRENCH TO ENGLISH TRANSLATOR. TRANSLATE THE USER'S SPEECH FROM FRENCH TO ENGLISH."
                "DO NOT RESPOND TO QUESTIONS, JUST TRANSLATE THE QUESTION ITSELF"
                "ONLY TRANSLATE IF THE USER IS SPEAKING IN FRENCH."
                "FOR NON FRENCH SPEAKERS, STAY SILENT AND DO NOT RESPOND."
            ),
        )

async def entrypoint(ctx: JobContext):
    logger.info(f"Starting agent session for room {ctx.room.name}")
    
    session = AgentSession(
        llm=openai.realtime.RealtimeModel(
            voice="ash",
            input_audio_transcription=None,  # Disable transcription
        )
    )

    # Create RoomIO instance for participant control
    room_io = RoomIO(session, room=ctx.room)
    await room_io.start()

    # Initially disable audio input
    session.input.set_audio_enabled(False)

    @session.on("input_speech_started")
    def on_input_speech_started():
        logger.info("User started speaking")

    @session.on("input_speech_stopped")
    def on_input_speech_stopped(ev):
        logger.info(f"User stopped speaking, transcription enabled: {ev.user_transcription_enabled}")

    @session.on("input_audio_transcription_completed")
    def on_input_transcription_completed(ev):
        logger.info(f"Received transcription: {ev.transcript} (final: {ev.is_final})")

    @session.on("speech_created")
    def on_speech_created(ev):
        logger.info(f"Agent started speaking, source: {ev.source}")

    @session.on("speech_finished")
    def on_speech_finished(ev):
        logger.info("Agent finished speaking")

    @ctx.room.on("track_published")
    def on_track_published(pub: RemoteTrackPublication, participant: RemoteParticipant):
        logger.info(f"Track published: {pub.kind} from {participant.identity}")
        if participant.identity == TARGET_PARTICIPANT:
            logger.info(f"Found target participant '{TARGET_PARTICIPANT}' publishing track")
            room_io.set_participant(participant.identity)
            session.input.set_audio_enabled(True)
            logger.info(f"Enabling audio input for participant '{TARGET_PARTICIPANT}'")

    @ctx.room.on("participant_connected")
    def on_participant_connected(participant):
        logger.info(f"Participant connected: {participant.identity}")
        logger.info(f"Participant metadata: {participant.metadata}")

    @ctx.room.on("track_subscribed")
    def on_track_subscribed(track, publication, participant):
        logger.info(f"Track subscribed: {track.kind} from {participant.identity}")
        logger.info(f"Track source: {publication.source}")
        if participant.identity == TARGET_PARTICIPANT:
            logger.info(f"Found target participant '{TARGET_PARTICIPANT}' publishing track")
            room_io.set_participant(participant.identity)
            session.input.set_audio_enabled(True)
            logger.info(f"Enabling audio input for participant '{TARGET_PARTICIPANT}'")

    @ctx.room.on("track_unsubscribed")
    def on_track_unsubscribed(track, publication, participant):
        logger.info(f"Track unsubscribed: {track.kind} from {participant.identity}")
        if participant.identity == TARGET_PARTICIPANT:
            room_io.unset_participant(participant.identity)
            session.input.set_audio_enabled(False)
            logger.info(f"Disabling audio input for participant '{TARGET_PARTICIPANT}'")

    await ctx.connect()
    logger.info("Connected to room")

    await session.start(
        agent=BahasaTranslator(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            audio_enabled=True,
            text_enabled=False,
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )
    logger.info("Agent session started successfully")

async def handle_request(request: JobRequest) -> None:
    logger.info(f"Handling request: {request}")
    await request.accept(
        identity="bahasa",
        # this attribute communicates to frontend that we support PTT
        attributes={"bahasa": "1"},
    )

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint,
                              request_fnc=handle_request,
                              agent_name="translator_id"
                            ))
