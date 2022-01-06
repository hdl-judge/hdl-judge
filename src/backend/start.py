import sys
import pytest
import uvicorn


if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] == "server":
        port = 8000
        if len(sys.argv) == 3:
            port = sys.argv[2]
        uvicorn.run("start_fastapi:app", host='0.0.0.0', port=port, reload=True, debug=True, workers=3)
    elif sys.argv[1] == "test":
        pytest.main(["-v", "--junitxml=/tmp/reports/pytest.xml", "-x", "tests"])
