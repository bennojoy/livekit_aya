'use client';

import {
  ControlBar,
  GridLayout,
  ParticipantTile,
  RoomAudioRenderer,
  useTracks,
  RoomContext,
  TrackReferenceOrPlaceholder,
  AudioTrack,
  ParticipantContextIfNeeded,
  TrackLoop,
  useParticipantContext,
  TrackRefContext,
  VideoTrack,
  ParticipantName,
  useGridLayout,
  TrackMutedIndicator,
  ConnectionQualityIndicator,
  MicIcon,
  MicDisabledIcon,
  ParticipantPlaceholder,
} from '@livekit/components-react';
import { Room, Track, RemoteTrackPublication } from 'livekit-client';
import { isTrackReference } from '@livekit/components-core';
import '@livekit/components-styles';
import { useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { useEffect } from 'react';
import React from 'react';




const serverUrl = process.env.NEXT_PUBLIC_LIVEKIT_URL;

export default function App() {
  const searchParams = useSearchParams();
  const room_name = searchParams.get('room');
  const identity = searchParams.get('identity');

  const [room] = useState(() => new Room({
    // Optimize video quality for each participant's screen
    adaptiveStream: true,
    // Enable automatic audio/video quality optimization
    dynacast: true,
  }));

  // Connect to room
  useEffect(() => {
    let mounted = true;
    
    const token = fetch(`/api/token?room=${room_name}&identity=${identity}`).then(res => res.json());
    token.then(data => {
      console.log("Token: ", data.token);
      try {
        room.connect(serverUrl, data.token);
      } catch (error) {
        console.error('Error connecting to room:', error);
      }
      console.log("Connected to room");
    });
    return () => {
      mounted = false;
      room.disconnect();
    };
  }, [room]);

  return (
    <RoomContext.Provider value={room}>
      <div data-lk-theme="default" style={{ 
        height: '100%', 
        width: '100%',
        backgroundColor: 'black',
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between'
      }}>
        <div style={{ 
          flex: 1, 
          position: 'relative',
          minHeight: 0,
          overflow: 'hidden'
        }}>
          <AyaConference />
        </div>
        <RoomAudioRenderer />
        <ControlBar style={{ 
          flexShrink: 0,
          height: '60px',
          zIndex: 10
        }} />
     </div> 
    </RoomContext.Provider>
  );



  function AyaParticipantTile({ trackRef, children }: { trackRef: TrackReferenceOrPlaceholder, children?: React.ReactNode }) {
    const participant = trackRef.participant;
    console.log("AyaParticipantTile: ", participant);
    const [isMuted, setIsMuted] = React.useState(false);

    // Create a track reference specifically for the microphone
    const audioTrackRef = {
      participant,
      source: Track.Source.Microphone,
      publication: participant.getTrackPublication(Track.Source.Microphone)
    };

    return (
      <ParticipantTile
        trackRef={trackRef}
        onParticipantClick={() => {
          console.log("Participant clicked: ", participant);
          setIsMuted(!isMuted);
        }}
        className="lk-participant-tile"
      >
        {isTrackReference(trackRef) && <VideoTrack trackRef={trackRef} />}
        <AudioTrack trackRef={audioTrackRef} muted={isMuted} />
        <div className="lk-participant-placeholder">
          <ParticipantPlaceholder />
        </div>
        <div className="lk-participant-metadata">
          <div className="lk-participant-metadata-item">
            <div className="lk-participant-metadata-item" data-lk-muted={isMuted}>
              {isMuted ? <MicDisabledIcon /> : <MicIcon />}
            </div>
            <ParticipantName />
          </div>
          <ConnectionQualityIndicator className="lk-participant-metadata-item" />
        </div>
      </ParticipantTile>
    );
  }

  function AyaConference() {
    console.log("AyaConference");
    const tracks = useTracks([
      { source: Track.Source.Camera, withPlaceholder: true }
    ],
    { onlySubscribed: false }
    );
    console.log("IN Aya Conference Tracks: ", tracks);
    
    const gridEl = React.useRef<HTMLDivElement>(null);
    const { layout } = useGridLayout(gridEl, tracks.length);
    
    return (
      <div ref={gridEl} className="lk-grid-layout" style={{ height: '100%', width: '100%' }}>
        <TrackLoop tracks={tracks}>
          <TrackRefContext.Consumer>
            {(trackRef) => (
              <ParticipantContextIfNeeded>
                <AyaParticipantTile trackRef={trackRef} />
              </ParticipantContextIfNeeded>
            )}
          </TrackRefContext.Consumer>
        </TrackLoop>
      </div>
    );
  }
 }