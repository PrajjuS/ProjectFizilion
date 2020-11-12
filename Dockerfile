FROM elytra8/projectfizilion:latest

RUN mkdir /Fizilion && chmod 777 /Fizilion
ENV PATH="/Fizilion/bin:$PATH"
WORKDIR /Fizilion

RUN git clone https://github.com/PrajwalS3/ProjectFizilion -b Experiment /Fizilion

#
# Copies session and config(if it exists)
#
COPY ./sample_config.env ./userbot.session* ./config.env* /One4uBot/

#transfer
RUN curl -sL https://git.io/file-transfer | sh 

#
# Finalization
#
CMD ["python3","-m","userbot"]
