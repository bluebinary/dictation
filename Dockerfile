# syntax = docker/dockerfile:1.4.0

FROM python:3.11

# Ensure pip has been upgraded to the latest version before installing dependencies
RUN pip install --upgrade pip

# Copy and install the dependencies from requirements.txt
COPY requirements.development.txt /app/requirements.development.txt
RUN pip install --requirement /app/requirements.development.txt

# COPY requirements.deployment.txt /app/requirements.deployment.txt
# RUN pip install --requirement /app/requirements.deployment.txt

# Copy the library source into the container's source folder for Black linting checks
COPY ./source/dictation /source/dictation

# Copy the README into the container's root folder for PyTest README code block testing
COPY ./README.md /README.md

# Copy the tests into the container's root folder for PyTest unit testing
COPY ./tests /tests

# Copy the library source into the container's site-packages folder for the unit tests
COPY ./source/dictation /usr/local/lib/python3.11/site-packages/dictation

# Create a custom entry point that allows us to override the command as needed
COPY <<"EOF" /entrypoint.sh
#!/bin/bash

ARGS=( "$@" );

echo -e "entrypoint.sh called with arguments: ${ARGS[@]} (service: ${SERVICE})";

if [[ "${ARGS[0]}" == "black" ]]; then
	echo -e "black ${ARGS[@]:1} /source /tests";
	black ${ARGS[@]:1} /source /tests;
elif [[ "${ARGS[0]}" == "pytest" ]]; then
	echo -e "pytest /tests ${ARGS[@]:1}";
	pytest /tests ${ARGS[@]:1};
	pytest --verbose --codeblocks /README.md;
elif [[ "${SERVICE}" == "black" ]]; then
	echo -e "black ${ARGS[@]} /source /tests";
	black ${ARGS[@]} /source /tests;
elif [[ "${SERVICE}" == "tests" ]]; then
	echo -e "pytest /tests ${ARGS[@]}";
	pytest /tests ${ARGS[@]};
	pytest --verbose --codeblocks /README.md;
else
	echo -e "No valid command was specified nor defined in the `SERVICE` environment!";
fi
EOF

RUN chmod +x /entrypoint.sh

# Run the unit tests starter shell script
ENTRYPOINT [ "/entrypoint.sh" ]
