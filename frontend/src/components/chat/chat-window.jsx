import React, { useState, useEffect, useRef } from "react";
import { ButtonSecondary } from "../ui/button-secondary/button-secondary";
import plusIcon from "../../images/plus.svg";
import styles from "./chat-window.module.css";
import { getChat } from "../../utils/api";


export const ChatWindow = ({ userId, onSubmitMessage }) => {
  const [newMessage, setNewMessage] = useState("");
  const chatSocketRef = useRef(null);
  const [messages, setMessages] = useState([]);
  const [basems, setBasems] = useState([]);
  const messageListRef = useRef(null);



  useEffect(() => {

    const token = localStorage.getItem("auth_token");
    const socketUrl =
      (window.location.protocol === "https:" ? "wss://" : "ws://") +
      window.location.host +
      "/ws/chat/" +
      (userId || '0') +
      `/?token=${token}`;

    chatSocketRef.current = new WebSocket(socketUrl);
    setMessages([]);
    chatSocketRef.current.onmessage = function (e) {
      const data = JSON.parse(e.data);
        setMessages(prevMessages => [
    ...prevMessages,
    { username: data.username, message: data.message }
  ]);
    };

    chatSocketRef.current.onclose = function (e) {
      console.error("Chat socket closed unexpectedly");
    };
    getChat( userId || '0', token)
    .then((data) => {
      setBasems(data);
    })
    .catch((error) => {
      console.error("Ошибка при получении списка сообщений:", error);
    });
    return () => {
      chatSocketRef.current.close();
    };
    
  }, [userId]);

  useEffect(() => {
    if (messageListRef.current) {
      messageListRef.current.scrollTop = messageListRef.current.scrollHeight;
    }
  }, [messages, basems]);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (newMessage.trim() !== "") {
      onSubmitMessage(newMessage);
      setNewMessage("");
    }
  };

  return (
    <div className={styles.container}>
      <ul className={styles.messageList} ref={messageListRef}>
      {basems.map((ms) => (
          <li key={ms.id} className={styles.messageItem}>
            <span className={styles.highlightedUsername}>{ms.username} : </span>{ms.message}
          </li>
        ))}
        {messages.map((message, index) => (
          <li key={index} className={styles.messageItem}>
            <span className={styles.highlightedUsername}>{message.username} : </span> {message.message} 
          </li>
        ))}

      </ul>
      <form className={styles.messageForm} onSubmit={handleSubmit}>
        <input
          type="text"
          className={styles.messageInput}
          value={newMessage}
          onChange={(event) => setNewMessage(event.target.value)}
          placeholder="Введите сообщение..."
        />
        <ButtonSecondary
          icon={plusIcon}
          type="submit"
          text="Отправить"
        />
      </form>
    </div>
  );
};