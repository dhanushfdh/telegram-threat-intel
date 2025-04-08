import json
from telethon.sync import TelegramClient
from telethon import functions, types
from datetime import datetime

# ================== CONFIGURATION ==================
SESSION_ID = "telegram_threatintel_session"
API_ID = ""
API_HASH = ""

# Load hashtags from external file
with open("hashtags.txt", "r") as f:
    hashtags = [line.strip() for line in f if line.strip()]

# Suspicious keywords for scam detection
SCAM_KEYWORDS = [
    "investment", "earn money", "crypto giveaway", "double your BTC",
    "forex trading", "instant profit", "binary options", "cash app",
    "airdrop", "win", "WIN", "Gaming"
]

# Output raw JSON file
RAW_JSON_FILE = f"raw_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
raw_data = []

# ================== TELEGRAM CLIENT ==================
with TelegramClient(SESSION_ID, API_ID, API_HASH) as client:
    for hashtag in hashtags:
        print(f"\n🔍 Searching for: #{hashtag}")

        try:
            result = client(functions.channels.SearchPostsRequest(
                hashtag=hashtag,
                offset_rate=0,
                offset_peer=types.InputPeerEmpty(),
                offset_id=0,
                limit=100
            ))
        except Exception as e:
            print(f"⚠️ Error searching posts for #{hashtag}: {e}")
            continue

        messages_list = []
        channel_cache = {}
        unique_messages = set()

        for message in result.messages:
            # Skip if empty or scam keywords found
            if not getattr(message, "message", None):
                continue

            if any(keyword.lower() in message.message.lower() for keyword in SCAM_KEYWORDS):
                print(f"⛔ Skipped scam message {message.id} in #{hashtag}")
                continue

            channel_id = None
            channel_name, channel_username = None, None

            # Get channel details if available
            if isinstance(message.peer_id, types.PeerChannel):
                channel_id = message.peer_id.channel_id

                if channel_id not in channel_cache:
                    try:
                        channel_entity = client.get_entity(types.PeerChannel(channel_id))
                        channel_cache[channel_id] = {
                            "name": channel_entity.title,
                            "username": channel_entity.username
                        }
                    except Exception as e:
                        print(f"⚠️ Error fetching channel details for ID {channel_id}: {e}")
                        continue

                channel_name = channel_cache[channel_id]["name"]
                channel_username = channel_cache[channel_id]["username"]

            # Skip duplicates
            message_signature = (message.id, message.message, message.date.isoformat())
            if message_signature in unique_messages:
                continue
            unique_messages.add(message_signature)

            # Get similar channels
            similar_channels = []
            if channel_username:
                try:
                    entity = client.get_input_entity(channel_username)
                    if isinstance(entity, (types.InputChannel, types.InputPeerChannel)):
                        input_channel = types.InputChannel(channel_id=entity.channel_id, access_hash=entity.access_hash)
                        similar_result = client(functions.channels.GetChannelRecommendationsRequest(channel=input_channel))

                        for ch in similar_result.chats:
                            similar_channels.append({
                                "username": ch.username,
                                "title": ch.title,
                                "id": ch.id
                            })
                except Exception as e:
                    print(f"⚠️ Error retrieving similar channels for @{channel_username}: {e}")

            # Prepare message data
            message_data = {
                "hashtag": hashtag,
                "message_id": message.id,
                "channel_id": channel_id,
                "channel_name": channel_name,
                "channel_username": channel_username,
                "post_author": getattr(message, "post_author", None),
                "date": message.date.isoformat(),
                "message": message.message,
                "media_present": message.media is not None,
                "media_type": type(message.media).__name__ if message.media else None,
                "views": message.views,
                "forwards": message.forwards,
                "replies": message.replies.replies if message.replies else 0,
                "hashtags": [
                    message.message[e.offset: e.offset + e.length]
                    for e in message.entities
                    if isinstance(e, types.MessageEntityHashtag)
                ] if message.entities else [],
                "entities": [
                    {
                        "type": type(e).__name__,
                        "offset": e.offset,
                        "length": e.length
                    } for e in message.entities
                ] if message.entities else [],
                "pinned": getattr(message, "pinned", False),
                "edit_date": message.edit_date.isoformat() if message.edit_date else None,
                "via_bot_id": getattr(message, "via_bot_id", None),
                "reply_to": getattr(message.reply_to, "reply_to_msg_id", None) if message.reply_to else None,
                "message_link": f"https://t.me/c/{channel_id}/{message.id}" if channel_id else None,
                "similar_channels": similar_channels
            }

            raw_data.append(message_data)

            print(f"✅ Collected message {message.id} from {channel_name} | Similar channels: {len(similar_channels)}")

    # Save raw JSON data to file
    with open(RAW_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=4)

    print(f"\n🎉 Data collection completed! Raw data saved to {RAW_JSON_FILE}")
