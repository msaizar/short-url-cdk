
# Welcome to the ShortURL project

## About

This is a work in progress to try out different AWS services.  The idea is to write a fully functional URL shortener. To make this work you'll need to modify the variables found at `app.py` and `toolchain/component.py`. Each stack located at `app.py` should have its own `hosted_zone_id` and `zone_name`, and each stack should be in its own account, with an already existing hosted zone. To install you can follow the installation instructions below.

### Deploying to a production account with a different CI CD account

`cdk bootstrap --trust <CI CD Account ID> --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess  aws://<PRODUCTION Account ID>/us-east-1 --profile ShortURL-Production`

`cdk bootstrap aws://<CI CD Account ID>/us-east-1 --profile ShortURL-CICD`

`cdk deploy ShortURLToolchain --profile ShortURL-CICD`

### Deploying to a staging environment

`cdk bootstrap aws://Staging Account ID>/us-east-1 --profile ShortURL-Staging`

`cdk deploy ShortURLStaging --profile ShortURL-Staging`

![Infrastructure](/images/diagram.png)

## Installation

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```sh
python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```sh
source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```sh
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```sh
pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```sh
cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

* `cdk ls`          list all stacks in the app
* `cdk synth`       emits the synthesized CloudFormation template
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk docs`        open CDK documentation

Enjoy!

## TODO

* Backend tests.
* Improve URL creation.
