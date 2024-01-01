import React, { useEffect, useState } from 'react';
import VideoCard from './VideoCard';
import axios from 'axios';
import LoadingSpinner from './LoadingSpinner';

interface VideoListProps {
  searchQuery: string;
}

const VideoList: React.FC<VideoListProps> = ({ searchQuery })  => {
  const [videos, setVideos] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log("ESTA ES LA BUSQUEDA AHORITA: /" + searchQuery + '/');
        setLoading(true);
        const encodedQuery = encodeURIComponent(searchQuery);
        const response = await axios.get("http://192.168.0.5:5000/data/", {
            params: { query: encodedQuery },
        });
        // const apiUrl = `http://127.0.0.1:8080/data/?query=${encodedQuery}`;
        // const response = await axios.get(apiUrl);
        setVideos(response.data.data);
        console.log(response.data)
      } catch (error) {
        console.error('Error fetching data from API', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [searchQuery]);

  return (
    <div className="videoList">
      {loading ? (
        <LoadingSpinner />
      ) : (
        videos.map((video) => (
          <VideoCard
            key={video.title}
            duration={'3:22'}
            imageUrl={video.video_miniature_public_url}
            videoUrl={video.video_public_url}
            title={video.title}
            labels={video.labels}
          />
        ))
      )}
    </div>
  );
};

export default VideoList;