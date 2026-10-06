# main.py
# Vital Forge
# Main entry point for the application.
#
# This file is intentionally kept simple.
# The actual screens, database operations, charts, data, and UI components
# are handled by their respective modules.

import tkinter as tk
from tkinter import messagebox

from config import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT
from database.connection import check_database_connection
from screens import VitalForgeApp


def center_window(window, width, height):
    """Place the application window in the center of the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")


def handle_startup_error(error):
    """Show a readable error if the application cannot start."""
    print("Vital Forge startup error:")
    print(error)

    try:
        error_window = tk.Tk()
        error_window.withdraw()

        messagebox.showerror(
            "Vital Forge - Startup Error",
            "Vital Forge could not start.\n\n"
            f"Error: {error}\n\n"
            "Please check the setup instructions in guides/BUILD.md."
        )

        error_window.destroy()

    except Exception:
        print("Unable to display the startup error window.")


def main():
    """Start Vital Forge."""
    try:
        root = tk.Tk()

        root.title(APP_NAME)

        center_window(
            root,
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )


        # Prevent the window from becoming too small.
        root.minsize(1000, 650)

        # Resolve the Supabase credential and verify MySQL before showing the app.
        connected, connection_error = check_database_connection()
        if not connected:
            messagebox.showwarning(
                "Database Unavailable",
                "Vital Forge could not verify its database connection.\n\n"
                f"{connection_error}",
                parent=root,
            )

        # Keep the application instance alive for the lifetime of the window.
        app = VitalForgeApp(root)

        # Close the application normally.
        root.protocol("WM_DELETE_WINDOW", root.destroy)

        root.mainloop()

    except Exception as error:
        handle_startup_error(error)


if __name__ == "__main__":
    main()