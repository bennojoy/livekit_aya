import { AccessToken, VideoGrant } from 'livekit-server-sdk';
import { NextRequest, NextResponse } from 'next/server';
import { RoomAgentDispatch, RoomConfiguration } from '@livekit/protocol';

// User to language mapping dictionary
const languageMap: { [key: string]: string } = {
  'john': 'en',
  'budi': 'id',
  'sarah': 'en',
  'aya': 'en',
  'ben': 'id'
};

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

    // Get language for the specific user identity
    const userLanguage = languageMap[identity.toLowerCase()] || 'en'; // default to 'en' if user not found
    const agentName = `translator_${userLanguage}`;

    at.roomConfig = new RoomConfiguration({
      agents: [
        new RoomAgentDispatch({
          agentName: agentName,
          metadata: JSON.stringify({ user_id: identity, language: userLanguage })
        })
      ]
    });

    const token = await at.toJwt();
    console.log('Generated token for room:', room, 'identity:', identity, 'agent:', agentName);
    
    return NextResponse.json({ token });
  } catch (error) {
    console.error('Error generating token:', error);
    return NextResponse.json(
      { error: 'Failed to generate token' },
      { status: 500 }
    );
  }
} 