# inherit prebuilt image
#Changed docker file
FROM elytra8/fizfed:latest

# env setup
RUN mkdir /Fizilion && chmod 777 /Fizilion
ENV PATH="/Fizilion/bin:$PATH"
WORKDIR /Fizilion

# clone repo
RUN git clone https://github.com/PrajjuS/ProjectFizilion -b demon /Fizilion
#RUN git clone https://github.com/Senpai-sama-afk/ProjectFizilion -b dragon /Fizilion

# Copies session and config(if it exists)
COPY ./sample_config.env ./userbot.session* ./config.env* /Fizilion/

#transfer
RUN curl -sL https://git.io/file-transfer | sh

# install required pypi modules
RUN pip3 install -r requirements.txt

# Finalization
CMD ["python3","-m","userbot"]
