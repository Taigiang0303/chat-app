"use client";

import { useAuth } from "@/hooks/use-auth";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { format } from "date-fns";

export default function ProfilePage() {
  const { user } = useAuth();

  // Format dates
  const formatDate = (dateString: string) => {
    try {
      return format(new Date(dateString), "PPP");
    } catch (error) {
      return "Unknown date";
    }
  };

  // Get user initials for avatar fallback
  const getUserInitials = () => {
    if (!user?.display_name) return "U";
    return user.display_name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase()
      .substring(0, 2);
  };

  return (
    <div className="container max-w-4xl py-10">
      <h1 className="mb-6 text-3xl font-bold">My Profile</h1>
      
      <div className="grid gap-6 md:grid-cols-[1fr_2fr]">
        {/* Profile Card */}
        <Card>
          <CardHeader className="flex flex-col items-center space-y-2 text-center">
            <Avatar className="h-24 w-24">
              <AvatarImage src={user?.profile_image_url} alt={user?.display_name} />
              <AvatarFallback className="text-xl">{getUserInitials()}</AvatarFallback>
            </Avatar>
            <div>
              <CardTitle>{user?.display_name}</CardTitle>
              <CardDescription className="text-sm">{user?.email}</CardDescription>
            </div>
          </CardHeader>
          <CardContent className="flex flex-col items-center space-y-4">
            <div className="w-full space-y-1 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Member since:</span>
                <span>{user?.created_at ? formatDate(user.created_at) : "Unknown"}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Last updated:</span>
                <span>{user?.updated_at ? formatDate(user.updated_at) : "Unknown"}</span>
              </div>
            </div>
            <Button className="w-full" asChild>
              <a href="/settings">Edit Profile</a>
            </Button>
          </CardContent>
        </Card>
        
        {/* Activity Card */}
        <Card>
          <CardHeader>
            <CardTitle>Account Activity</CardTitle>
            <CardDescription>
              Your recent activity and account statistics
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-8">
              <div className="space-y-2">
                <h3 className="text-lg font-medium">Statistics</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div className="rounded-lg border p-3">
                    <div className="text-sm font-medium text-muted-foreground">Total Messages</div>
                    <div className="text-2xl font-bold">0</div>
                  </div>
                  <div className="rounded-lg border p-3">
                    <div className="text-sm font-medium text-muted-foreground">Conversations</div>
                    <div className="text-2xl font-bold">0</div>
                  </div>
                </div>
              </div>
              
              <div className="space-y-2">
                <h3 className="text-lg font-medium">Recent Activity</h3>
                <div className="rounded-lg border p-4">
                  <p className="text-center text-muted-foreground">No recent activity to display</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
} 