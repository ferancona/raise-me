
## TODO
- [ ] Class to interact with yaml files.
- [ ] Perhaps, class to interact with bash commands easily (e.g. retrieve output of command with constant output) 


- [ ] Deploy module
    - [X] Wait until OpenWhisk installation is done.
    - [X] Setup Wsk CLI
        - [X] Get AWS load balancer's DNS and assign as apihost.
        - [X] Test Wsk CLI
        - [ ] Check whether tests can run successfully (running wsk commands through the shell works in Powershell but not on Git Bash)
    - [ ] GCPDeployer class
        - [ ] Setup Kubernetes cluster (GKE)
        - [ ] Automate deployment
            - [ ] Deploy manually
            - [ ] Implement raise_me.deploy.GCPDeployer


- [ ] Make a plan for the rest of the project!
    - Before working on parsing module, define what needs to be built!

- Why is my Wsk deployment only accepting http endpoints (and not https)?

- [ ] Builder module
    - [ ] What exactly do I have to build?
        - [ ] Manual testing
            - [X] Trigger Lambda from S3 event using AWS EventBridge.
            - [ ] From Lambda, make api call to OpenWhisk.
                - [X] Using Python (requests module).
                - [ ] Using JavaScript Client.
        - [X] Create an Action that invokes Lambda function.
            - [X] Invoke Action from Lambda.
            - [X] Invoke Lambda from Action.

        - Event Buses (in AWS EventBridge and Google Pub/Sub)
        - Wsk Actions that connect to AWS EventBridge and Google Pub/Sub.
            - Which would be the best way to implement a Wsk python interface? Through a Command class? Wsk class that uses a Command class? (Check https://github.com/apache/openwhisk-client-python) Would it make sense to use JavaScript to make it easier? Do I actually have to?
        - What in Google Pub/Sub?

- [ ] Parser module
    - [ ] 
    - [ ] Google research on how to create a parser? In python?
    - [ ] Validate resource existence (How in AWS? And GCP?)
        - [ ] AWS
        - [ ] GCP

- [ ] CLI Tool
    - [ ] Identify concretely required commands and arguments (add docs)
        - [ ] Add documentation
    - [ ] Implement CLI interface
        - [ ] 

- [ ] Tests (Pytest)


- [ ] Logging module (or configuration).
- [ ] Class to create/validate certificates.
- [ ] Use python's kubernetes-client (https://github.com/kubernetes-client/python).
