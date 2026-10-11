import sys
import os

# Cloud Platform Port Sanitizer (fixes Railway literal '$PORT' CLI argument bug)
for i, arg in enumerate(sys.argv):
    if arg == "--port" and i + 1 < len(sys.argv):
        val = str(sys.argv[i + 1]).strip()
        if not val.isdigit():
            # If literal '$PORT', '${PORT}', or empty string, resolve from environment
            resolved_port = os.environ.get("PORT", "8000")
            if not str(resolved_port).isdigit():
                resolved_port = "8000"
            sys.argv[i + 1] = str(resolved_port)
