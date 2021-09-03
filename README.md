## Set up

* Install:

  ```shell
  git clone git@github.com:dtgoitia/t.git
  cd t/

  # Create and activate Python virtual environment
  python3 -m venv .venv
  . .venv/bin/activate

  # install repo dependencies locally
  make install
  ```

* Configuration (mandatory):

  At `~/.config/t/config.jsonc`:

  ```json
  {
    "projects": [
      {
        "id": 1234,
        "name": "Name of the project",
        "entries": ["Task 1", "Task 2"]
      }
    ]
  }
  ```

* Credentials (mandatory):

  At `~/.config/t/credentials.jsonc`:

  ```jsonc
  {
    // Get API token at https://track.toggl.com/profile
    "toggle_api_token": "_____INSERT_API_TOKEN_HERE_____"
  }
  ```
