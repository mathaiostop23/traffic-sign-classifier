# 🚦 Traffic Sign Classifier

An AI-powered web application that classifies traffic signs using deep learning. Built with Flask, TensorFlow, and modern web technologies.

![Traffic Sign Classifier](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.1-green)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.19.0-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **🤖 AI-Powered Classification**: Recognizes 43 different types of traffic signs
- **📱 Modern UI**: Responsive design with dark/light theme support
- **📁 Drag & Drop Upload**: Easy file upload with validation
- **📊 Confidence Scores**: Shows prediction confidence and alternatives
- **📸 Gallery**: View history of all predictions
- **⚡ Real-time Results**: Instant classification results
- **🔒 Secure**: Input validation and sanitization

## 🎯 Supported Traffic Signs

The model can classify 43 different traffic sign categories including:

- Speed limits (20, 30, 50, 60, 70, 80, 100, 120 km/h)
- Warning signs (dangerous curves, slippery road, pedestrians, etc.)
- Regulatory signs (stop, yield, no entry, no passing, etc.)
- Mandatory signs (turn directions, roundabout, keep right/left)

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- pip package manager
- Git

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/traffic-sign-classifier.git
   cd traffic-sign-classifier
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   ```
   http://localhost:5001
   ```

## 🐳 Docker Deployment

### Using Docker

1. **Build the image**
   ```bash
   docker build -t traffic-sign-classifier .
   ```

2. **Run the container**
   ```bash
   docker run -p 5001:5001 traffic-sign-classifier
   ```

### Using Docker Compose

1. **Create docker-compose.yml**
   ```yaml
   version: '3.8'
   services:
     traffic-classifier:
       build: .
       ports:
         - "5001:5001"
       volumes:
         - ./static/uploads:/app/static/uploads
       environment:
         - FLASK_ENV=production
   ```

2. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

## 📁 Project Structure

```
traffic-sign-classifier/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── README.md             # Project documentation
├── image_history.json    # Prediction history
├── ml_model/
│   ├── traffic_sign.h5   # Trained TensorFlow model
│   └── traffic_sign.keras
├── templates/
│   ├── index.html        # Homepage
│   ├── result.html       # Results page
│   └── gallery.html      # Gallery page
├── static/
│   ├── css/
│   │   └── style.css     # Modern styling
│   ├── js/
│   │   └── main.js       # Interactive features
│   └── uploads/          # User uploaded images
```

## 🛠️ Technology Stack

- **Backend**: Flask (Python 3.12)
- **AI/ML**: TensorFlow 2.19, OpenCV
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Styling**: Custom CSS with CSS Grid/Flexbox
- **Icons**: Font Awesome 6
- **Fonts**: Inter (Google Fonts)

## 🔧 Configuration

### Environment Variables

```bash
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=production  # or development
FLASK_DEBUG=False

# Application Settings
UPLOAD_FOLDER=static/uploads/
MAX_CONTENT_LENGTH=10485760  # 10MB
```

### Model Configuration

The application uses a pre-trained CNN model:
- **Architecture**: Convolutional Neural Network
- **Input Size**: 32x32 RGB images
- **Classes**: 43 traffic sign categories
- **Accuracy**: 95%+ on validation set

## 📖 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Homepage with upload form |
| `/predict` | POST | Upload and classify image |
| `/gallery` | GET | View prediction history |
| `/prediction/<id>` | GET | View specific prediction |

## 🎨 Usage Examples

### Basic Classification

1. **Upload an image**: Drag and drop or click to select
2. **View results**: See classification with confidence score
3. **Check alternatives**: View other possible classifications
4. **Browse history**: Access previous predictions in gallery

### API Usage (if extended)

```python
import requests

# Upload image for classification
files = {'file': open('traffic_sign.jpg', 'rb')}
response = requests.post('http://localhost:5001/predict', files=files)
result = response.json()
```

## 🔧 Development

### Setting up Development Environment

1. **Clone and install**
   ```bash
   git clone <repository>
   cd traffic-sign-classifier
   pip install -r requirements.txt
   ```

2. **Run in development mode**
   ```bash
   export FLASK_ENV=development
   export FLASK_DEBUG=True
   python app.py
   ```

3. **File structure for development**
   - Edit templates in `templates/`
   - Modify styles in `static/css/style.css`
   - Update JavaScript in `static/js/main.js`

### Adding New Features

- **New templates**: Add to `templates/` directory
- **Static files**: Place in appropriate `static/` subdirectory
- **Routes**: Add to `app.py`
- **Styling**: Extend `style.css` with CSS custom properties

## 🧪 Testing

### Manual Testing

1. **Test different image formats**: JPG, PNG, WEBP
2. **Test file size limits**: Max 10MB
3. **Test responsiveness**: Mobile, tablet, desktop
4. **Test themes**: Light and dark mode

### Image Formats Supported

- **JPEG/JPG**: Standard format
- **PNG**: With transparency support
- **WEBP**: Modern format

## 🚀 Deployment Options

### Local Development
```bash
python app.py  # Runs on http://localhost:5001
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

### Docker Production
```bash
docker build -t traffic-classifier .
docker run -p 5001:5001 traffic-classifier
```

### Cloud Deployment

The application can be deployed to:
- **Heroku**: Using Procfile
- **AWS ECS**: Using Docker
- **Google Cloud Run**: Container deployment
- **DigitalOcean**: App Platform

## 🔒 Security Features

- **Input validation**: File type and size checking
- **Secure uploads**: Filename sanitization
- **Non-root container**: Docker security best practices
- **CORS protection**: Flask security headers

## 📊 Performance

- **Model inference**: < 2 seconds
- **File upload**: Supports up to 10MB
- **Concurrent users**: Scales with container resources
- **Memory usage**: ~1GB with TensorFlow model loaded

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   lsof -i :5001  # Find process using port
   kill <PID>     # Kill the process
   ```

2. **Module not found**
   ```bash
   pip install -r requirements.txt
   ```

3. **Model file not found**
   - Ensure `ml_model/traffic_sign.h5` exists
   - Check file permissions

4. **Docker issues**
   ```bash
   docker system prune  # Clean up Docker
   docker build --no-cache -t traffic-classifier .
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Mathaios**
- GitHub: [@mathaios](https://github.com/mathaios)
- Portfolio: [Your Portfolio](https://your-portfolio.com)

## 🙏 Acknowledgments

- TensorFlow team for the ML framework
- German Traffic Sign Recognition Benchmark dataset
- Flask community for the web framework
- Font Awesome for icons
- Google Fonts for typography

## 📈 Future Enhancements

- [ ] Real-time video classification
- [ ] Mobile app version
- [ ] REST API with authentication
- [ ] Model performance analytics
- [ ] Multi-language support
- [ ] Batch processing
- [ ] Cloud storage integration

---

Made with ❤️ using Python, TensorFlow, and Flask 