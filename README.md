
### Example
```yaml
events:    
  s3-to-cloudfunction:
    source:
      provider: aws
      filters: # AWS EventBridge event patterns or GCP Eventrac filters.
        - 'source: ["aws.s3"]'
        - 'detail-type: ["Object Created"]'
        - 'detail: {"bucket": {"name": ["my-bucket-name"]}}'
    targets:
      - http:
            method: get
            url: my-cloudfunction-url
      - action:
            name: my-openwhisk-action-name
```
Action targets are your own user-defined Actions deployed in [Apache OpenWhisk](https://openwhisk.apache.org/) that are triggered when the event defined in 'source' is raised.

-----

### Roadmap
- [X] Parser module
- [X] Builder module
    - [X] OpenWhisk resources
    - [X] Cloud resources
        - [X] AWS
            - [X] Eventbridge
            - [X] Lambda
        - [X] GCP
            - [X] Eventrac
            - [X] Workflows
- [ ] CLI Tool
- [ ] Tests
- [ ] Add setup instructions (e.g., enabling google services)


#### Future features
- [ ] Logging