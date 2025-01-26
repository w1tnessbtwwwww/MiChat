import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './panel.css';

import OnChat from '../../assets/onIcon/onChat.svg';
import OnStg from '../../assets/onIcon/onSettin.svg';

import DarkOffChat from '../../assets/dark-theme-icon/offChat.svg';
import DarkOffStg from '../../assets/dark-theme-icon/offSettin.svg';
import DarkProfile from '../../assets/dark-theme-icon/profile.svg';

import LightOffChat from '../../assets/light-theme-icon/offChat.svg';
import LightOffStg from '../../assets/light-theme-icon/offSettin.svg';
import LightProfile from '../../assets/light-theme-icon/profile.svg';

const Panel: React.FC = () => {
  const [isChatActive, setIsChatActive] = useState(false);
  const [isSettingsActive, setIsSettingsActive] = useState(false);
  const [isDarkTheme, setIsDarkTheme] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (location.pathname === '/chats') {
      setIsChatActive(true);
    } else {
      setIsChatActive(false);
    }

    if (location.pathname === '/settings') {
      setIsSettingsActive(true);
    } else {
      setIsSettingsActive(false);
    }
  }, [location]);

  useEffect(() => {
    const updateTheme = () => {
      const bodyClass = document.body.classList.contains('dark') ? 'dark' : 'light';
      setIsDarkTheme(bodyClass === 'dark');
    };

    // Initial check
    updateTheme();

    // Add event listener for class changes
    const observer = new MutationObserver(updateTheme);
    observer.observe(document.body, { attributes: true, attributeFilter: ['class'] });

    // Cleanup on component unmount
    return () => {
      observer.disconnect();
    };
  }, []);

  const handleChatClick = () => {
    navigate('/chats'); // Переход на страницу чатов
  };

  const handleSettingsClick = () => {
    navigate('/settings'); // Переход на страницу настроек
  };

  const offChat = isDarkTheme ? DarkOffChat : LightOffChat;
  const offStg = isDarkTheme ? DarkOffStg : LightOffStg;
  const profile = isDarkTheme ? DarkProfile : LightProfile;

  return (
    <div className="panel">
      <img
        src={isChatActive ? OnChat : offChat}
        alt="chat"
        onClick={handleChatClick}
      />
      <img src={profile} alt="profile" />
      <img
        src={isSettingsActive ? OnStg : offStg}
        alt="settings"
        onClick={handleSettingsClick}
      />
    </div>
  );
};

export default Panel;
