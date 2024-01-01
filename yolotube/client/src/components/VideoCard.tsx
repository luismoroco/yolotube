import { useNavigate } from "react-router-dom";

interface VideoCardProps {
  title: string;
  duration: string;
  imageUrl: string;
  videoUrl: string;
  labels: []
}

const VideoCard: React.FC<VideoCardProps> = ({ title, duration, imageUrl, videoUrl, labels }) => {
  const navigate = useNavigate()
  
  const handleClick = () => {
    const labelsString = Object.keys(labels).map(label => `#${label}`).join(' ');
    console.log(title);
    console.log(videoUrl);
    console.log(labelsString);
    
    navigate(`/media/${encodeURIComponent(title)}/${encodeURIComponent(videoUrl)}/${encodeURIComponent(labelsString)}`);
  };

  return (
    <div className="videoCard" onClick={handleClick} style={{ cursor: 'pointer' }}>
      <div className="videoCard__thumbnail">
        <img src={imageUrl} alt={title} />
        <span className="videoCard__duration">{duration}</span>
      </div>
      <div className="videoCard__info">
        <h3 className="videoCard__title">{title}</h3>
      </div>
    </div>
  );
}

export default VideoCard;