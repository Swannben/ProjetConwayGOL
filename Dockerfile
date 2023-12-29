
# Use the official Python image as the base image
FROM nogil/python

# Set the working directory inside the container
WORKDIR /app

# Copy the ConwayGOLFineGrainParalellism file to the working directory
COPY ConwayGOLFineGrainParalellism /app/ConwayGOLFineGrainParalellism


RUN pip install numpy

# Set the entry point to run the ConwayGOLFineGrainParalellism file
ENTRYPOINT ["python", "ConwayGOLFineGrainParalellism"]
