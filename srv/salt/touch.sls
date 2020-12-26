command:
  cmd.run:
    - name: touch /tmp/test
    - unless: test -f /tmp/test
