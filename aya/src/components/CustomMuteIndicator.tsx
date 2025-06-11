import React from 'react';
import { MicIcon, MicDisabledIcon } from '@livekit/components-react';

interface CustomMuteIndicatorProps {
  isMuted: boolean;
}

export function CustomMuteIndicator({ isMuted }: CustomMuteIndicatorProps) {
  return (
    <div className="lk-participant-metadata-item" data-lk-muted={isMuted}>
      {isMuted ? <MicDisabledIcon /> : <MicIcon />}
    </div>
  );
} 