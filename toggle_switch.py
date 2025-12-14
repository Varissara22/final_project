import tkinter as tk

class ToggleSwitch(tk.Canvas):
    
    def __init__(self, parent, width=100, height=40, 
                 bg_on="#3b82f6", bg_off="#6b7280",
                 knob_color="#ffffff",
                 text_on="ON", text_off="OFF",
                 text_color="#ffffff",
                 command=None, initial_state=False, **kwargs):

        kwargs.pop('background', None)
        
        super().__init__(
            parent, 
            width=width, 
            height=height,
            bg=parent.cget('bg') if hasattr(parent, 'cget') else '#252836',
            highlightthickness=0,
            **kwargs
        )
        
        self.width = width
        self.height = height
        self.bg_on = bg_on
        self.bg_off = bg_off
        self.knob_color = knob_color
        self.text_on = text_on
        self.text_off = text_off
        self.text_color = text_color
        self.command = command
        
        self._is_on = initial_state
        self._animating = False
        
        self.corner_radius = height // 2
        self.knob_radius = (height // 2) - 3
        self.padding = 2
        
        self.knob_off_x = self.corner_radius - 2
        self.knob_on_x = width - self.corner_radius + 2
        self.current_knob_x = self.knob_on_x if self._is_on else self.knob_off_x
        
        self.animation_steps = 15
        self.animation_delay = 10  
        
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
        self._draw()
    
    def _draw(self):
        self.delete("all")
        
        progress = (self.current_knob_x - self.knob_off_x) / (self.knob_on_x - self.knob_off_x)
        bg_color = self._interpolate_color(self.bg_off, self.bg_on, progress)
        
        self._create_rounded_rect(
            0, 0, self.width, self.height,
            radius=self.corner_radius,
            fill=bg_color,
            outline="",
            tags="background"
        )
        
        if self._is_on or progress > 0.5:
            font_size = 7 if len(self.text_on) > 5 else 8
            text_x = self.knob_on_x - self.knob_radius - 18 
            self.create_text(
                text_x,  
                self.height // 2,
                text=self.text_on,
                fill=self.text_color,
                font=("Segoe UI", font_size, "bold"),
                anchor="e", 
                tags="text"
            )
        else:
            font_size = 7 if len(self.text_off) > 5 else 8
            text_x = self.knob_off_x + self.knob_radius + 18
            self.create_text(
                text_x,  
                self.height // 2,
                text=self.text_off,
                fill=self.text_color,
                font=("Segoe UI", font_size, "bold"),
                anchor="w", 
                tags="text"
            )
        
        knob_y = self.height // 2
        self.create_oval(
            self.current_knob_x - self.knob_radius,
            knob_y - self.knob_radius,
            self.current_knob_x + self.knob_radius,
            knob_y + self.knob_radius,
            fill=self.knob_color,
            outline="#d1d5db",
            width=1,
            tags="knob"
        )
    
    def _create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius, y1,
            x1 + radius, y1,
            x2 - radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def _interpolate_color(self, color1, color2, progress):
        r1, g1, b1 = self._hex_to_rgb(color1)
        r2, g2, b2 = self._hex_to_rgb(color2)
        
        r = int(r1 + (r2 - r1) * progress)
        g = int(g1 + (g2 - g1) * progress)
        b = int(b1 + (b2 - b1) * progress)
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _on_click(self, event=None):
        if not self._animating:
            self.toggle()
    
    def _on_enter(self, event=None):
        self.config(cursor="hand2")
    
    def _on_leave(self, event=None):
        self.config(cursor="")
    
    def toggle(self):
        if self._animating:
            return
        
        self._is_on = not self._is_on
        
        self._animate_to_state()
        
        if self.command:
            self.command(self._is_on)
    
    def _animate_to_state(self):
        target_x = self.knob_on_x if self._is_on else self.knob_off_x
        start_x = self.current_knob_x
        distance = target_x - start_x
        
        if distance == 0:
            return
        
        step_size = distance / self.animation_steps
        self._animating = True
        self._animate_step(start_x, target_x, step_size, 0)
    
    def _animate_step(self, start_x, target_x, step_size, current_step):
        if current_step >= self.animation_steps:
            self.current_knob_x = target_x
            self._animating = False
            self._draw()
            return
        
        progress = current_step / self.animation_steps
        eased_progress = 1 - pow(1 - progress, 3)
        self.current_knob_x = start_x + (target_x - start_x) * eased_progress

        self._draw()
        
        self.after(
            self.animation_delay,
            lambda: self._animate_step(start_x, target_x, step_size, current_step + 1)
        )
    
    def is_on(self): 
        return self._is_on
    
    def get_state(self):
        return self._is_on
    
    def set_state(self, state, animate=True):
        if self._is_on == state:
            return 
        
        self._is_on = state
        
        if animate:
            self._animate_to_state()
        else:
            self.current_knob_x = self.knob_on_x if state else self.knob_off_x
            self._draw()
    
    def enable(self):
        self.bind("<Button-1>", self._on_click)
    
    def disable(self):
        self.unbind("<Button-1>")
        self.config(cursor="")

