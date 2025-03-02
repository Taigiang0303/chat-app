import * as React from "react";

export default function AboutPage() {
  return (
    <div className="container mx-auto py-12 px-4">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-4xl font-bold mb-6">About Our Chat Application</h1>
        
        <section className="mb-10">
          <h2 className="text-2xl font-semibold mb-4">Our Mission</h2>
          <p className="text-lg text-muted-foreground mb-4">
            Our mission is to create a seamless and secure communication platform that connects people across the globe. We believe in the power of real-time communication to bridge distances and bring people together.
          </p>
          <p className="text-lg text-muted-foreground">
            Whether you're connecting with friends, family, or colleagues, our chat application provides the tools you need for effective and enjoyable conversations.
          </p>
        </section>
        
        <section className="mb-10">
          <h2 className="text-2xl font-semibold mb-4">Technology Stack</h2>
          <p className="text-lg text-muted-foreground mb-4">
            Our application is built using cutting-edge technologies to ensure performance, security, and scalability:
          </p>
          <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
            <li><span className="font-medium">Frontend:</span> Next.js, React, TypeScript, Tailwind CSS</li>
            <li><span className="font-medium">Backend:</span> FastAPI, Python</li>
            <li><span className="font-medium">Database:</span> PostgreSQL with Supabase</li>
            <li><span className="font-medium">Real-time Communication:</span> WebSockets</li>
            <li><span className="font-medium">Authentication:</span> JWT, OAuth</li>
          </ul>
        </section>
        
        <section className="mb-10">
          <h2 className="text-2xl font-semibold mb-4">Privacy & Security</h2>
          <p className="text-lg text-muted-foreground mb-4">
            We take your privacy and security seriously. All messages are encrypted end-to-end, ensuring that only you and your intended recipients can read them.
          </p>
          <p className="text-lg text-muted-foreground">
            Our application adheres to industry best practices for data protection and complies with relevant privacy regulations.
          </p>
        </section>
        
        <section>
          <h2 className="text-2xl font-semibold mb-4">Our Team</h2>
          <p className="text-lg text-muted-foreground mb-6">
            We are a dedicated team of developers, designers, and product specialists passionate about creating the best communication tools possible.
          </p>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
            {teamMembers.map((member) => (
              <div key={member.name} className="border rounded-lg p-4 text-center">
                <div className="w-24 h-24 rounded-full bg-muted mx-auto mb-4 flex items-center justify-center">
                  <span className="text-2xl font-bold">{member.initials}</span>
                </div>
                <h3 className="font-bold text-lg">{member.name}</h3>
                <p className="text-muted-foreground">{member.role}</p>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

const teamMembers = [
  { name: "Jane Doe", role: "Lead Developer", initials: "JD" },
  { name: "John Smith", role: "UX Designer", initials: "JS" },
  { name: "Emily Chen", role: "Backend Engineer", initials: "EC" },
  { name: "Michael Brown", role: "Product Manager", initials: "MB" },
  { name: "Sarah Johnson", role: "DevOps Engineer", initials: "SJ" },
  { name: "David Kim", role: "Frontend Developer", initials: "DK" },
]; 