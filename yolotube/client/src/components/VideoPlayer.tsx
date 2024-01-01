import { useParams } from 'react-router-dom';


const VideoPlayer: React.FC = () => {
    const { title, url, description } = useParams();
    console.log(title, url, description);
    
    return (
        <div className="videoPlayer">
        <div className="videoPlayer__video" style={{ height: '100%', width: '100%' }}>
            <video controls width="100%" height="100%">
            <source src={url} type="video/mp4" />
            Tu navegador no admite el elemento de video.
            </video>
        </div>
        <div className="videoPlayer__description" style={{ height: '30%' }}>
            {title} <br/>
            {description} 
        </div>
        </div>
    );
};

export default VideoPlayer;