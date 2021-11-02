## Set up

* Prerequisites:

  - `podman` must be installed and [configured][1]

* Install:

  ```shell
  git clone git@github.com:dtgoitia/t.git
  cd t/

  make install-container
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

<!-- External references -->

[1]: https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md#etcsubuid-and-etcsubgid-configuration "Set up sub user IDs and sub group IDs"
