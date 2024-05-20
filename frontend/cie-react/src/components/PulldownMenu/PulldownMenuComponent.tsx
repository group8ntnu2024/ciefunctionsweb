import React from 'react';
import './PulldownMenu.css';
import { useContentController } from '../../hooks/useContentController';

export const PulldownMenu: React.FC = () => {
  const { setSelectedOption } = useContentController();

  return (
    <div className="pulldownMenu">
      <select className="pulldownSelect" onChange={(e) => setSelectedOption(e.target.value)}>
        <option value="method1">CIE LMS cone fundamentals</option>
        <option value="method2">CIE LMS cone fundamentals (9 sign. figs.)</option>
        <option value="method3">MacLeod-Boynton Is chromaticity diagram</option>
        <option value="method4">Maxwellian Im chromaticity diagram</option>
        <option value="method5">CIE XYZ cone-fundamental-based tristimulus functions</option>
        <option value="method6">CIE xy cone-fundamental-based chromaticity diagram</option>
        <option value="method7">XYZ cone-fundamental-based tristimulus functions for purple-line stimuli</option>
        <option value="method8">xy cone-fundamental-based chromaticity diagram (purple-line stimuli)</option>
        <option value="method9">CIE XYZ standard colour-matching functions</option>
        <option value="method10">CIE xy standard chromaticity diagram</option>
      </select>
    </div>
  );
};