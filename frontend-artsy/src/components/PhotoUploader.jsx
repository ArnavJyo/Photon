// src/components/PhotoUploader.js
import React, { useState, useRef, useEffect } from "react";
import { Container, Row, Col, Form } from "react-bootstrap";
import Dropzone from "react-dropzone";
import "../App.css";
const PhotoUploader = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const canvasRef = useRef(null);

  const handleFileDrop = (acceptedFiles) => {
    const file = acceptedFiles[0];
    setSelectedFile(file);
    setProcessedImage(null);
  };
  const handleUpload = async (buttonText) => {
    if (!selectedFile) {
      console.error("No file selected");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);
    formData.append("buttonText", buttonText);

    try {
      const response = await fetch("http://localhost:5000/process-image", {
        method: "POST",
        body: formData,
      });
      if (response.ok) {
        const result = await response.json();
        console.log(result.processed_image_path);
        setProcessedImage(result.processed_image_path);
      } else {
        console.error("Failed to process image");
      }
    } catch (error) {
      console.error("Error processing image:", error);
    }
  };
  const getImageDataUrl = (pixelData) => {
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");

    // Assuming each sub-array in pixelData is a row of pixel values
    canvas.width = pixelData[0].length;
    canvas.height = pixelData.length;

    for (let y = 0; y < pixelData.length; y++) {
      for (let x = 0; x < pixelData[y].length; x++) {
        const [r, g, b] = pixelData[y][x];
        ctx.fillStyle = `rgba(${r},${g},${b},255)`;
        ctx.fillRect(x, y, 1, 1);
      }
    }

    // Convert the canvas to a base64-encoded data URL
    const dataUrl = canvas.toDataURL("image/png");

    return dataUrl;
  };
  const resizeImage = (image) => {
    return new Promise((resolve) => {
      const maxSize = 500;
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");

      const img = new Image();
      img.src = URL.createObjectURL(image);

      img.onload = () => {
        let width = img.width;
        let height = img.height;

        if (width > maxSize || height > maxSize) {
          if (width > height) {
            height = (maxSize / width) * height;
            width = maxSize;
          } else {
            width = (maxSize / height) * width;
            height = maxSize;
          }
        }

        canvas.width = width;
        canvas.height = height;

        ctx.drawImage(img, 0, 0, width, height);
        canvas.toBlob(
          (blob) => {
            resolve(new File([blob], "resized_image", { type: "image/jpeg" }));
          },
          "image/jpeg",
          1
        );
      };
    });
  };

  const drawImageOnCanvas = async () => {
    if (canvasRef.current && selectedFile) {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");
      if (processedImage) {
        const processedImg = new Image();
        processedImg.src = getImageDataUrl(processedImage);

        processedImg.onload = () => {
          // Clear previous drawings
          ctx.clearRect(0, 0, canvas.width, canvas.height);

          // Calculate the center coordinates
          const centerX = canvas.width / 2 - processedImg.width / 2;
          const centerY = canvas.height / 2 - processedImg.height / 2;

          // Draw the processed image on the center of the canvas
          ctx.drawImage(processedImg, centerX, centerY);
        };
      } else {
        const resizedImage = await resizeImage(selectedFile);
        const img = new Image();
        img.src = URL.createObjectURL(resizedImage);

        img.onload = () => {
          // Clear previous drawings
          ctx.clearRect(0, 0, canvas.width, canvas.height);

          // Calculate the center coordinates
          const centerX = canvas.width / 2 - img.width / 2;
          const centerY = canvas.height / 2 - img.height / 2;

          // Draw the image on the center of the canvas
          ctx.drawImage(img, centerX, centerY);
        };
      }
    }
  };

  // Redraw the image on canvas whenever the selectedFile changes
  useEffect(() => {
    drawImageOnCanvas();
  }, [selectedFile, processedImage]);

  return (
    <Container>
      <Row className='mt-5'>
        <Col xs={12} className='text-center'>
          <h2>Photo Uploader</h2>
          <Form>
            <Form.Group controlId='formFile' className='mb-3'>
              <Dropzone onDrop={handleFileDrop}>
                {({ getRootProps, getInputProps }) => (
                  <div {...getRootProps()} className='dropzone text-center'>
                    <input {...getInputProps()} />
                    <p>Drag & drop a photo here, or click to select one</p>
                  </div>
                )}
              </Dropzone>
            </Form.Group>
          </Form>
        </Col>
      </Row>
      <Row className='mt-3'>
        <Col xs={9} className='text-center'>
          {selectedFile && (
            <div>
              <div
                style={{
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  height: "100vh",
                }}
              >
                <canvas
                  ref={canvasRef}
                  width={1000} // Adjust the canvas width as needed
                  height={500} // Adjust the canvas height as needed
                  style={{ border: "1px solid #000" }}
                />
                <div className='task-bar'>
                  <div className='dropdown'>
                    <button className='dropbtn'>DistanceMetric</button>
                    <div className='dropdown-content'>
                      <button onClick={() => handleUpload("Euclidean")}>
                        Euclidean
                      </button>
                      <button onClick={() => handleUpload("Minkowski")}>
                        Minkowski
                      </button>
                      <button onClick={() => handleUpload("Manhattan")}>
                        Manhattan
                      </button>
                      <button onClick={() => handleUpload("Chebyshev")}>
                        Chebyshev
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </Col>
      </Row>
    </Container>
  );
};

export default PhotoUploader;