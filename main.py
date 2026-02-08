"""
Private Video Player - Android Version
A mobile video player with playlist support (no camera features)
"""
import os
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock
from functools import partial


class VideoPlayerWidget(BoxLayout):
    """Custom video player widget."""
    
    def __init__(self, player_index=0, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.player_index = player_index
        self.current_file = None
        self.playlist = []
        self.current_playlist_index = -1
        self.autoplay = True
        
        # Video player
        self.video = VideoPlayer(
            state='stop',
            options={'eos': 'loop', 'allow_stretch': True}
        )
        self.video.bind(state=self.on_video_state)
        self.add_widget(self.video)
        
        # Controls
        controls = BoxLayout(size_hint_y=0.1, spacing=5, padding=5)
        
        self.next_btn = Button(text='Next', size_hint_x=0.3)
        self.next_btn.bind(on_press=self.play_next)
        controls.add_widget(self.next_btn)
        
        self.autoplay_btn = Button(text='Auto: ON', size_hint_x=0.3)
        self.autoplay_btn.bind(on_press=self.toggle_autoplay)
        controls.add_widget(self.autoplay_btn)
        
        self.add_widget(controls)
    
    def on_video_state(self, instance, value):
        """Handle video state changes."""
        if value == 'stop' and self.autoplay and self.current_file:
            # Video ended, play next
            Clock.schedule_once(lambda dt: self.play_next(), 0.5)
    
    def toggle_autoplay(self, *args):
        """Toggle autoplay mode."""
        self.autoplay = not self.autoplay
        self.autoplay_btn.text = f'Auto: {"ON" if self.autoplay else "OFF"}'
    
    def set_video(self, file_path):
        """Set the video file to play."""
        if os.path.exists(file_path):
            self.current_file = file_path
            self.video.source = file_path
            self.video.state = 'play'
            
            # Update playlist index
            if file_path in self.playlist:
                self.current_playlist_index = self.playlist.index(file_path)
    
    def play_next(self, *args):
        """Play the next video in the playlist."""
        if not self.playlist:
            return
        
        self.current_playlist_index = (self.current_playlist_index + 1) % len(self.playlist)
        next_video = self.playlist[self.current_playlist_index]
        self.set_video(next_video)
    
    def set_playlist(self, playlist):
        """Set the playlist for this player."""
        self.playlist = playlist
        if playlist and not self.current_file:
            self.current_playlist_index = 0
            self.set_video(playlist[0])


class PlaylistPanel(BoxLayout):
    """Playlist management panel."""
    
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.playlist = []
        self.on_video_selected = None
        
        # Header
        header = BoxLayout(size_hint_y=0.08, spacing=5, padding=5)
        header.add_widget(Label(text='Playlist', bold=True))
        
        add_btn = Button(text='+ Files', size_hint_x=0.3)
        add_btn.bind(on_press=self.add_files)
        header.add_widget(add_btn)
        
        clear_btn = Button(text='Clear', size_hint_x=0.3)
        clear_btn.bind(on_press=self.clear_playlist)
        header.add_widget(clear_btn)
        
        self.add_widget(header)
        
        # Playlist items
        self.scroll = ScrollView()
        self.playlist_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.playlist_layout.bind(minimum_height=self.playlist_layout.setter('height'))
        self.scroll.add_widget(self.playlist_layout)
        self.add_widget(self.scroll)
    
    def add_files(self, *args):
        """Show file chooser to add videos."""
        content = BoxLayout(orientation='vertical')
        
        # File chooser
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])
            path = '/storage/emulated/0/'
        else:
            path = os.path.expanduser('~')
        
        filechooser = FileChooserListView(
            path=path,
            filters=['*.mp4', '*.mkv', '*.avi', '*.mov', '*.wmv', '*.flv', '*.webm', '*.m4v']
        )
        content.add_widget(filechooser)
        
        # Buttons
        buttons = BoxLayout(size_hint_y=0.1, spacing=5)
        
        def add_selected(*args):
            for file_path in filechooser.selection:
                self.add_to_playlist(file_path)
            popup.dismiss()
        
        add_btn = Button(text='Add Selected')
        add_btn.bind(on_press=add_selected)
        buttons.add_widget(add_btn)
        
        cancel_btn = Button(text='Cancel')
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        buttons.add_widget(cancel_btn)
        
        content.add_widget(buttons)
        
        popup = Popup(title='Select Videos', content=content, size_hint=(0.9, 0.9))
        popup.open()
    
    def add_to_playlist(self, file_path):
        """Add a video file to the playlist."""
        if file_path not in self.playlist:
            self.playlist.append(file_path)
            
            # Create playlist item button
            btn = Button(
                text=os.path.basename(file_path),
                size_hint_y=None,
                height=60
            )
            btn.bind(on_press=partial(self._on_video_click, file_path))
            self.playlist_layout.add_widget(btn)
    
    def _on_video_click(self, file_path, *args):
        """Handle video item click."""
        if self.on_video_selected:
            self.on_video_selected(file_path)
    
    def clear_playlist(self, *args):
        """Clear the playlist."""
        self.playlist.clear()
        self.playlist_layout.clear_widgets()
    
    def get_playlist(self):
        """Get the current playlist."""
        return self.playlist.copy()


class MainApp(BoxLayout):
    """Main application layout."""
    
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        # Toolbar
        toolbar = BoxLayout(size_hint_y=0.08, spacing=5, padding=5)
        
        toolbar.add_widget(Label(text='Layout:', size_hint_x=0.3))
        
        self.layout_spinner = Spinner(
            text='1 Video',
            values=['1 Video', '2 Videos', '4 Videos'],
            size_hint_x=0.5
        )
        self.layout_spinner.bind(text=self.on_layout_change)
        toolbar.add_widget(self.layout_spinner)
        
        self.toggle_playlist_btn = Button(text='☰', size_hint_x=0.2)
        self.toggle_playlist_btn.bind(on_press=self.toggle_playlist)
        toolbar.add_widget(self.toggle_playlist_btn)
        
        self.add_widget(toolbar)
        
        # Main content area
        self.main_area = BoxLayout(orientation='horizontal')
        
        # Video grid
        self.video_grid = GridLayout(cols=1, spacing=5, padding=5)
        
        # Create video players
        self.video_players = []
        for i in range(4):
            player = VideoPlayerWidget(player_index=i)
            self.video_players.append(player)
        
        # Add first player by default
        self.video_grid.add_widget(self.video_players[0])
        
        self.main_area.add_widget(self.video_grid)
        
        # Playlist panel
        self.playlist_panel = PlaylistPanel(size_hint_x=0.35)
        self.playlist_panel.on_video_selected = self.on_video_selected
        self.main_area.add_widget(self.playlist_panel)
        
        self.add_widget(self.main_area)
        
        self.playlist_visible = True
    
    def on_layout_change(self, spinner, text):
        """Handle layout change."""
        self.video_grid.clear_widgets()
        
        if text == '1 Video':
            self.video_grid.cols = 1
            self.video_grid.add_widget(self.video_players[0])
        elif text == '2 Videos':
            self.video_grid.cols = 2
            self.video_grid.add_widget(self.video_players[0])
            self.video_grid.add_widget(self.video_players[1])
        elif text == '4 Videos':
            self.video_grid.cols = 2
            for i in range(4):
                self.video_grid.add_widget(self.video_players[i])
        
        # Update all players with the playlist
        playlist = self.playlist_panel.get_playlist()
        for player in self.video_players:
            player.set_playlist(playlist)
    
    def toggle_playlist(self, *args):
        """Toggle playlist visibility."""
        if self.playlist_visible:
            self.main_area.remove_widget(self.playlist_panel)
            self.playlist_visible = False
        else:
            self.main_area.add_widget(self.playlist_panel)
            self.playlist_visible = True
    
    def on_video_selected(self, file_path):
        """Handle video selection from playlist."""
        # Play in first visible player
        if self.video_grid.children:
            for child in reversed(self.video_grid.children):
                if isinstance(child, VideoPlayerWidget):
                    child.set_video(file_path)
                    break


class PrivatePlayerApp(App):
    """Main application class."""
    
    def build(self):
        """Build the application UI."""
        Window.clearcolor = (0.07, 0.07, 0.07, 1)
        return MainApp()


if __name__ == '__main__':
    PrivatePlayerApp().run()
