import { useState, useEffect } from 'react';
import axios from 'axios';
import styles from '../styles/Home.module.css';

export default function Home() {
  const [text, setText] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [debouncedText, setDebouncedText] = useState('');

  useEffect(() => {
    const delay = 500; // Delay in milliseconds
    const timeoutId = setTimeout(() => {
      setDebouncedText(text);
    }, delay);

    return () => {
      clearTimeout(timeoutId);
    };
  }, [text]);

  useEffect(() => {
    const fetchResponse = async () => {
      if (debouncedText) {
        try {
          const response = await axios.post(
            'http://localhost:8000/sdxl_streaming',
            { content: debouncedText },
            { responseType: 'blob' }
          );

          const imageBlob = response.data;
          const imageObjectUrl = URL.createObjectURL(imageBlob);
          setImageUrl(imageObjectUrl);
        } catch (error) {
          console.error('Error fetching response:', error);
        }
      }
    };
    fetchResponse();
  }, [debouncedText]);

  const handleChange = (e) => {
    setText(e.target.value);
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Stable Diffusion Stream</h1>
      <input className={styles.inputField} type="text" value={text} onChange={handleChange} />
      {imageUrl && <img className={styles.image} src={imageUrl} alt="Generated" />}
    </div>
  );
}
