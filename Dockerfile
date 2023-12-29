
# Use the official Python image as the base image
FROM nogil/python

# Set the working directory inside the container
WORKDIR /app

# Copy the ConwayGOLLargeGrainParalellism file to the working directory
COPY ConwayGOLLargeGrainParalellism.py /app/ConwayGOLLargeGrainParalellism.py


RUN pip install numpy

# Set the entry point to run the ConwayGOLFineGrainParalellism file
ENTRYPOINT ["python", "ConwayGOLLargeGrainParalellism.py"]
