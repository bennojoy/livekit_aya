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
)
from livekit.plugins import (
    openai,
    noise_cancellation,
)

logger = logging.getLogger("bahasa-translator")
logger.setLevel(logging.INFO)

load_dotenv()

class EnglishTranslator(Agent):
    def __init__(self) -> None:
        super().__init__(
             instructions=(
                "You are a professional English to Indonesian translator."
                 "ONLY TRANSLATE AND RESPOND WITH THE TRANSLATION IF THE USER IS SPEAKING IN ENGLISH."
                "DO NOT TRANSLATE AND RESPOND  WITH TRANSLATION IF THE USER  IS NOT SPEAKING IN ENGLISH, STAY SILENT AND DO NOT RESPOND."
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

    @ctx.room.on("connection_state_changed")
    def on_connection_state(state):
        logger.info(f"Room connection state changed: {state}")

    @ctx.room.on("participant_connected")
    def on_participant_connected(participant):
        logger.info(f"Participant connected: {participant.identity}")
        logger.info(f"Participant metadata: {participant.metadata}")

    @ctx.room.on("track_subscribed")
    def on_track_subscribed(track, publication, participant):
        logger.info(f"Track subscribed: {track.kind} from {participant.identity}")
        logger.info(f"Track source: {publication.source}")

    @ctx.room.on("track_unsubscribed")
    def on_track_unsubscribed(track, publication, participant):
        logger.info(f"Track unsubscribed: {track.kind} from {participant.identity}")

    await session.start(
        agent=EnglishTranslator(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            audio_enabled=True,
            text_enabled=False,
            noise_cancellation=noise_cancellation.BVC(),
        ),
  
    )
    logger.info("Agent session started successfully")
    
    await ctx.connect()
    logger.info("Connected to room")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
