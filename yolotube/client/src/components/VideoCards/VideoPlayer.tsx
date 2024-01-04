import { useParams } from 'react-router-dom';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import LabelCard from './LabelCard';
import Slider from 'react-slick';

const VideoPlayer: React.FC = () => {
    const { title, url, description } = useParams();
    
    const responseVideo_url = url?.replace(/\?/g, '%3F');
    console.log(`title: ${title}\n URL: ${responseVideo_url}\n labels: ${description}`);

    let labelMap: { [key: string]: number } = {};

    if (description !== undefined) {
        try {
          const jsonString = description.match(/\{.*\}/)?.[0] || '';
          labelMap = JSON.parse(jsonString);
        } catch (error) {
          console.error('Error al analizar JSON:', error);
        }
      }

      const entries = Object.entries(labelMap);
      entries.sort((a, b) => b[1] - a[1]);
      const sortedLabelMap = Object.fromEntries(entries);
      console.log(sortedLabelMap);

    const sliderSettings = {
        useCSS: true,
        infinite: false,
        slidesToShow: 4,
        slidesToScroll: 3,
        speed: 1000
    };



    return (
        <div className="videoPlayer">
            <div className="videoPlayer__video">
                <video controls>
                <source src={responseVideo_url} type="video/mp4" />
                Tu navegador no admite el elemento de video.
                </video>
            </div>
            <div className="videoPlayer__description">
                <div className='videoPlayer_title'>
                    {title} <br/>
                </div>
                <div className='videoPlayer_tags'>
                    <Slider {...sliderSettings}>
                        {Object.entries(sortedLabelMap).map(([key, value]) => (
                        <LabelCard 
                            key={key}
                            count={value}
                            label={key}
                        />
                        ))}
                    </Slider>
                </div>
                
            </div>
        </div>
    );
};

export default VideoPlayer;