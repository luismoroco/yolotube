import React from 'react';
import './css/LabelCard.css'
interface LabelCardProps {
  label: string;
  count: number;
}

const LabelCard: React.FC<LabelCardProps> = ({ label, count }) => (
  <div className="card">
    <div className='card_title'>
      {label}: {count}
    </div>
  </div>
);

export default LabelCard;