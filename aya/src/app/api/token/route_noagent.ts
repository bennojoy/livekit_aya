import { AccessToken, VideoGrant } from 'livekit-server-sdk';
import { NextRequest, NextResponse } from 'next/server';
import { RoomAgentDispatch, RoomConfiguration } from '@livekit/protocol';

export async function GET(request: NextRequest) {
  const apiKey = process.env.LIVEKIT_API_KEY;
  const apiSecret = process.env.LIVEKIT_API_SECRET;

  if (!apiKey || !apiSecret) {
    return NextResponse.json(
      { error: 'Server misconfigured' },
      { status: 500 }
    );
  }

  // Get room and identity from query params
  const { searchParams } = new URL(request.url);
  const room = searchParams.get('room');
  const identity = searchParams.get('identity');

  if (!room || !identity) {
    return NextResponse.json(
      { error: 'Room and identity are required' },
      { status: 400 }
    );
  }

  try {
    const at = new AccessToken(apiKey, apiSecret, {
      identity,
    });

    const videoGrant: VideoGrant = {
      room,
      roomJoin: true,
      canPublish: true,
      canSubscribe: true,
    };

    at.addGrant(videoGrant);

 {/*}   at.roomConfig = new RoomConfiguration({
      agents: [
        new RoomAgentDispatch({
          agentName: "translator",
          metadata: '{"user_id": "12345"}'
        })
      ]
    });
 */}


    const token = await at.toJwt();
    console.log('Generated token for room:', room, 'identity:', identity);
    
    return NextResponse.json({ token });
  } catch (error) {
    console.error('Error generating token:', error);
    return NextResponse.json(
      { error: 'Failed to generate token' },
      { status: 500 }
    );
  }
} 