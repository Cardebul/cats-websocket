import React, { useState, useEffect, useRef } from "react";
import { ButtonSecondary } from "../ui/button-secondary/button-secondary";
import plusIcon from "../../images/plus.svg";
import styles from "./chat-window.module.css";

export const ChatWindow = ({ initialMessages, userId, onSubmitMessage }) => {
  console.log(initialMessages);
  const [newMessage, setNewMessage] = useState("");
  const chatSocketRef = useRef(null);
  const [messages, setMessages] = useState([]);


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
      setMessages((prevMessages) => [...prevMessages, data.message]);
    };

    chatSocketRef.current.onclose = function (e) {
      console.error("Chat socket closed unexpectedly");
    };

    return () => {
      chatSocketRef.current.close();
    };
  }, [userId]);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (newMessage.trim() !== "") {
      onSubmitMessage(newMessage);
      setNewMessage("");
    }
  };

  return (
    <div className={styles.container}>
      <ul className={styles.messageList}>
        {messages.map((message, index) => (
          <li key={index} className={styles.messageItem}>
            {message}
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