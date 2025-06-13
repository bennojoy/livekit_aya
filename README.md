# LiveKit Audio/Video Room Application

This is a real-time audio and video room application built with LiveKit, Next.js, and Python. It supports both audio-only and video-enabled rooms with features like muting participants and connection quality indicators.

## Features

- Audio-only rooms with visualization
- Video-enabled rooms with camera controls
- Participant muting functionality
- Connection quality indicators
- Real-time audio/video streaming
- Python-based agent integration

## Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- npm (comes with Node.js)
- LiveKit server

## Installation

### Automatic Setup

Run the setup script which will install all necessary dependencies:

```bash
python setup.py
```

The script will:
1. Check and install Node.js if needed
2. Install Python dependencies
3. Set up the Next.js project
4. Create necessary configuration files

### Manual Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Next.js dependencies:
```bash
cd aya
npm install
```

3. Create `.env.local` file in the `aya` directory with your LiveKit configuration:
```
NEXT_PUBLIC_LIVEKIT_URL=ws://localhost:7880
NEXT_PUBLIC_LIVEKIT_API_KEY=devkey
NEXT_PUBLIC_LIVEKIT_API_SECRET=secret
```

## Running the Application

1. Start the LiveKit server

2. Run the Python agent:
   - For English agent:
   ```bash
   python livekit_agent_english.py
   ```
   - For Bahasa agent (with specific room and debug logging):
   ```bash
   python livekit_agent_bahasa.py connect --room=test-room --log-level=debug
   ```

3. Start the Next.js development server:
```bash
cd aya
npm run dev
```

4. Open http://localhost:3000 in your browser

## Project Structure

- `aya/` - Next.js application
  - `src/app/audioroom/` - Audio-only room implementation
  - `src/app/videoroom/` - Video-enabled room implementation
  - `src/components/` - Reusable components
- `livekit_agent_english.py` - English language agent
- `livekit_agent_bahasa.py` - Bahasa language agent
- `setup.py` - Installation script

## Development

- Audio room: http://localhost:3000/audioroom
- Video room: http://localhost:3000/videoroom


### NGROK SETUP for ssl termination

1. curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
  && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
  | sudo tee /etc/apt/sources.list.d/ngrok.list \
  && sudo apt update \
  && sudo apt install ngrok
  in mac: brew install ngrok

2. ngrok config add-authtoken <token>
    

3.ngrok http http://localhost:3000
 



## License

This project is licensed under the MIT License - see the LICENSE file for details. 