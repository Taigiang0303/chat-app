"use client";

import * as React from "react";
import { useEffect, useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { ScrollArea } from "@/components/ui/scroll-area";
import { cn } from "@/lib/utils";

interface Message {
  id: string;
  content: string;
  sender: "user" | "other";
  timestamp: Date;
  senderName: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      content: "Hello! How can I help you today?",
      sender: "other",
      timestamp: new Date(),
      senderName: "Support",
    },
  ]);
  const [newMessage, setNewMessage] = useState("");
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    const message: Message = {
      id: Date.now().toString(),
      content: newMessage,
      sender: "user",
      timestamp: new Date(),
      senderName: "You",
    };

    setMessages((prev) => [...prev, message]);
    setNewMessage("");

    // Simulate a response after 1 second
    setTimeout(() => {
      const response: Message = {
        id: (Date.now() + 1).toString(),
        content: "Thanks for your message! This is a demo response.",
        sender: "other",
        timestamp: new Date(),
        senderName: "Support",
      };
      setMessages((prev) => [...prev, response]);
    }, 1000);
  };

  // Scroll to bottom when messages change
  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="container mx-auto py-6">
      <div className="grid grid-cols-1 md:grid-cols-[300px_1fr] gap-6">
        <div className="hidden md:block border rounded-lg p-4">
          <h2 className="text-xl font-bold mb-4">Contacts</h2>
          <div className="space-y-2">
            <div className="flex items-center space-x-3 p-2 rounded-md bg-accent">
              <Avatar>
                <AvatarImage src="/avatars/support.png" />
                <AvatarFallback>SP</AvatarFallback>
              </Avatar>
              <div>
                <p className="font-medium">Support</p>
                <p className="text-sm text-muted-foreground">Online</p>
              </div>
            </div>
            {["Alice", "Bob", "Charlie"].map((name) => (
              <div
                key={name}
                className="flex items-center space-x-3 p-2 rounded-md hover:bg-accent cursor-pointer"
              >
                <Avatar>
                  <AvatarFallback>{name.slice(0, 2).toUpperCase()}</AvatarFallback>
                </Avatar>
                <div>
                  <p className="font-medium">{name}</p>
                  <p className="text-sm text-muted-foreground">Offline</p>
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className="flex flex-col border rounded-lg h-[calc(100vh-theme(spacing.32))]">
          <div className="border-b p-4">
            <div className="flex items-center space-x-3">
              <Avatar>
                <AvatarImage src="/avatars/support.png" />
                <AvatarFallback>SP</AvatarFallback>
              </Avatar>
              <div>
                <p className="font-medium">Support</p>
                <p className="text-sm text-muted-foreground">Online</p>
              </div>
            </div>
          </div>
          <ScrollArea className="flex-1 p-4" ref={scrollAreaRef}>
            <div className="space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={cn(
                    "flex",
                    message.sender === "user" ? "justify-end" : "justify-start"
                  )}
                >
                  <div
                    className={cn(
                      "max-w-[80%] rounded-lg p-3",
                      message.sender === "user"
                        ? "bg-primary text-primary-foreground"
                        : "bg-muted"
                    )}
                  >
                    <div className="flex items-center space-x-2 mb-1">
                      <span className="font-medium text-sm">
                        {message.senderName}
                      </span>
                      <span className="text-xs opacity-70">
                        {message.timestamp.toLocaleTimeString([], {
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                      </span>
                    </div>
                    <p>{message.content}</p>
                  </div>
                </div>
              ))}
            </div>
          </ScrollArea>
          <div className="border-t p-4">
            <form onSubmit={handleSendMessage} className="flex space-x-2">
              <Input
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                placeholder="Type your message..."
                className="flex-1"
              />
              <Button type="submit">Send</Button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
} 