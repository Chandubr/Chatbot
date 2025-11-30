export function connectWebSocket(url,onMessage) 
{
    const socket = new WebSocket(url);

    socket.onopen = () => {
        console.log("WebSocket connection established.");
    }
    socket.onmessage = (event) => {
        if(onMessage)
        onMessage(event.data);
    }
    socket.onclose = () => {
        console.log("WebSocket connection closed.");
    }
    socket.onerror = (error) => {
        console.error("WebSocket error:", error);
    }   

    return socket;
}