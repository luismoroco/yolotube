import { useNavigate } from "react-router-dom";

interface VideoCardProps {
  title: string;
  duration: number;
  imageUrl: string;
  videoUrl: string;
  labels: []
}

function secsToMinSecs(secs: number) {
  const minutos = Math.floor(secs / 60);
  const segundosRestantes = secs % 60;
  const formatoMinutos = minutos < 10 ? `0${minutos}` : minutos;
  const formatoSegundos = segundosRestantes < 10 ? `0${segundosRestantes}` : segundosRestantes;

  return `${formatoMinutos}:${formatoSegundos}`;
}

const VideoCard: React.FC<VideoCardProps> = ({ title, duration, imageUrl, videoUrl, labels }) => {
  
  const navigate = useNavigate()
  const min_secs_format = secsToMinSecs(duration-1);
  const responseImage_url = imageUrl?.replace(/\?/g, '%3F');
  const labelsString = JSON.stringify(labels);
  const handleClick = () => {
    navigate(`/media/${encodeURIComponent(title)}/${encodeURIComponent(videoUrl)}/${(labelsString)}`);
  };

  return (
    <div className="videoCard" onClick={handleClick} style={{ cursor: 'pointer' }}>
      <div className="videoCard__thumbnail">
        <img src={responseImage_url} alt={title} />
        <span className="videoCard__duration">{min_secs_format}</span>
      </div>
      <div className="videoCard__info">
        <h3 className="videoCard__title">{title}</h3>
      </div>
    </div>
  );
}

export default VideoCard;