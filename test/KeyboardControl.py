import keyboard

def main():
    print("Press 'Q' to quit.")
    
    # Create a set to keep track of currently pressed keys
    pressed_keys = set()
    
    while True:
        event = keyboard.read_event()
        
        if event.event_type == keyboard.KEY_DOWN:
            key = event.name
            if key == 'q':
                break
            pressed_keys.add(key)
        elif event.event_type == keyboard.KEY_UP:
            key = event.name
            pressed_keys.discard(key)
        
        print(f"Pressed keys: {', '.join(pressed_keys)}")

if __name__ == "__main__":
    main()
