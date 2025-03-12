import unittest
from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch
import json
import discord
from stage0_py_utils import DiscordBot

class TestDiscordBot(unittest.IsolatedAsyncioTestCase):
    
    async def asyncSetUp(self):
        """Set up a mock bot instance before each test."""
        self.mock_handle_command = MagicMock()
        self.mock_handle_message = MagicMock()
        self.mock_handle_command.return_value = ["12345"]  # Default active channel
        
        self.bot = DiscordBot(
            handle_command_function=self.mock_handle_command,
            handle_message_function=self.mock_handle_message,
            bot_id="BOT-123"
        )

        # Properly patch `self.bot.user`
        self.bot._user = MagicMock()
        type(self.bot).user = PropertyMock(return_value=self.bot._user)  # Correctly mock user property

        # Set initial active channels list
        self.bot.active_channels = ["12345"]

    @patch.object(discord.TextChannel, 'send', new_callable=AsyncMock)
    async def test_on_ready_loads_active_channels(self, mock_send):
        """Test that the bot loads active channels on startup."""
        self.mock_handle_command.return_value = ["12345", "67890"]
        
        await self.bot.on_ready()

        self.mock_handle_command.assert_called_once_with(f"/bot/get_channels/{json.dumps('BOT-123', separators=(',', ':'))}")
        self.assertEqual(self.bot.active_channels, ["12345", "67890"])

    async def test_on_message_processes_active_channel_message(self):
        """Test that the bot processes messages from active channels."""
        message = MagicMock()
        message.guild = True
        message.channel.id = "12345"  
        message.author = MagicMock()
        message.author.id = "USER-1"
        message.author.name = "Alice"
        message.content = "Hello bot!"
        message.channel.send = AsyncMock()  

        self.mock_handle_message.return_value = "Hello Alice!"

        await self.bot.on_message(message)

        self.mock_handle_message.assert_called_once_with(channel='12345', user='Alice', role='user', dialog='group', text='Hello bot!')
        message.channel.send.assert_called_once_with("Hello Alice!")

    async def test_on_message_ignores_self_messages(self):
        """Ensure bot ignores its own messages."""
        message = MagicMock()
        message.author = self.bot.user  # Message from the bot itself
        message.channel.send = AsyncMock()

        await self.bot.on_message(message)

        self.mock_handle_message.assert_not_called()
        message.channel.send.assert_not_called()

    async def test_on_message_handles_join_command(self):
        """Test that the bot joins a channel when @mention join is used."""
        message = MagicMock()
        message.guild = True
        message.channel.id = "67890"
        message.author = MagicMock()
        message.author.id = "USER-2"
        message.author.username = "Bob"
        message.content = "@bot join"
        message.mentions = [self.bot.user]
        message.channel.send = AsyncMock()  
        
        self.mock_handle_command.return_value = ["12345", "67890"]  # Updated channel list

        await self.bot.on_message(message)

        self.mock_handle_command.assert_called_once_with(f"/bot/add_channel/{json.dumps({'bot_id': 'BOT-123', 'channel_id': '67890'}, separators=(',', ':'))}")
        message.channel.send.assert_called_once_with("✅ Channel: 67890 added to active channels list.")
        self.assertIn("67890", self.bot.active_channels)

    async def test_on_message_handles_leave_command(self):
        """Test that the bot leaves a channel when @mention leave is used."""
        message = MagicMock()
        message.guild = True
        message.channel.id = "12345"
        message.author = MagicMock()
        message.author.id = "USER-3"
        message.author.username = "Charlie"
        message.content = "@bot leave"
        message.mentions = [self.bot.user]
        message.channel.send = AsyncMock()  

        self.mock_handle_command.return_value = ["67890"]  

        await self.bot.on_message(message)

        self.mock_handle_command.assert_called_once_with(f"/bot/remove_channel/{json.dumps({'bot_id': 'BOT-123', 'channel_id': '12345'}, separators=(',', ':'))}")
        message.channel.send.assert_called_once_with("✅ Channel: 12345 removed from active channels list.")
        self.assertNotIn("12345", self.bot.active_channels)

if __name__ == "__main__":
    unittest.main()