"use client";

import { useState } from "react";
import { useAuth } from "@/hooks/use-auth";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Switch } from "@/components/ui/switch";
import { toast } from "sonner";

export default function SettingsPage() {
  const { user } = useAuth();
  const [isSubmitting, setIsSubmitting] = useState(false);

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

  const handleProfileUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      toast.success("Profile updated successfully");
    } catch (error) {
      toast.error("Failed to update profile");
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handlePasswordUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      toast.success("Password updated successfully");
    } catch (error) {
      toast.error("Failed to update password");
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="container max-w-4xl py-10">
      <h1 className="mb-6 text-3xl font-bold">Settings</h1>
      
      <Tabs defaultValue="profile" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="profile">Profile</TabsTrigger>
          <TabsTrigger value="account">Account</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
        </TabsList>
        
        {/* Profile Tab */}
        <TabsContent value="profile">
          <Card>
            <CardHeader>
              <CardTitle>Profile Settings</CardTitle>
              <CardDescription>
                Update your profile information visible to other users
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleProfileUpdate} className="space-y-6">
                <div className="flex flex-col items-center space-y-4 sm:flex-row sm:space-x-4 sm:space-y-0">
                  <Avatar className="h-24 w-24">
                    <AvatarImage src={user?.profile_image_url} alt={user?.display_name} />
                    <AvatarFallback className="text-xl">{getUserInitials()}</AvatarFallback>
                  </Avatar>
                  <div className="flex flex-col space-y-2">
                    <Button type="button" variant="outline" size="sm">
                      Change Avatar
                    </Button>
                    <Button type="button" variant="ghost" size="sm" className="text-destructive">
                      Remove Avatar
                    </Button>
                  </div>
                </div>
                
                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="display_name">Display Name</Label>
                    <Input id="display_name" defaultValue={user?.display_name} />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="email">Email</Label>
                    <Input id="email" type="email" defaultValue={user?.email} disabled />
                  </div>
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="bio">Bio</Label>
                  <Textarea id="bio" placeholder="Tell us about yourself" className="min-h-[100px]" />
                </div>
                
                <CardFooter className="flex justify-end px-0">
                  <Button type="submit" disabled={isSubmitting}>
                    {isSubmitting ? "Saving..." : "Save Changes"}
                  </Button>
                </CardFooter>
              </form>
            </CardContent>
          </Card>
        </TabsContent>
        
        {/* Account Tab */}
        <TabsContent value="account">
          <Card>
            <CardHeader>
              <CardTitle>Account Settings</CardTitle>
              <CardDescription>
                Manage your account security and preferences
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Password Section */}
              <div>
                <h3 className="mb-4 text-lg font-medium">Change Password</h3>
                <form onSubmit={handlePasswordUpdate} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="current_password">Current Password</Label>
                    <Input id="current_password" type="password" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="new_password">New Password</Label>
                    <Input id="new_password" type="password" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="confirm_password">Confirm New Password</Label>
                    <Input id="confirm_password" type="password" />
                  </div>
                  <Button type="submit" disabled={isSubmitting}>
                    {isSubmitting ? "Updating..." : "Update Password"}
                  </Button>
                </form>
              </div>
              
              {/* Danger Zone */}
              <div className="rounded-md border border-destructive/50 p-4">
                <h3 className="mb-4 text-lg font-medium text-destructive">Danger Zone</h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium">Delete Account</p>
                      <p className="text-sm text-muted-foreground">
                        Permanently delete your account and all your data
                      </p>
                    </div>
                    <Button variant="destructive">Delete Account</Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        
        {/* Notifications Tab */}
        <TabsContent value="notifications">
          <Card>
            <CardHeader>
              <CardTitle>Notification Settings</CardTitle>
              <CardDescription>
                Manage how and when you receive notifications
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div className="space-y-4">
                  <h3 className="text-lg font-medium">Email Notifications</h3>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <div className="space-y-0.5">
                        <Label htmlFor="new_message">New Messages</Label>
                        <p className="text-sm text-muted-foreground">
                          Receive emails when you get new messages
                        </p>
                      </div>
                      <Switch id="new_message" defaultChecked />
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div className="space-y-0.5">
                        <Label htmlFor="new_user">New Users</Label>
                        <p className="text-sm text-muted-foreground">
                          Receive emails when new users join
                        </p>
                      </div>
                      <Switch id="new_user" />
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div className="space-y-0.5">
                        <Label htmlFor="marketing">Marketing</Label>
                        <p className="text-sm text-muted-foreground">
                          Receive emails about new features and updates
                        </p>
                      </div>
                      <Switch id="marketing" />
                    </div>
                  </div>
                </div>
                
                <div className="space-y-4">
                  <h3 className="text-lg font-medium">Push Notifications</h3>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <div className="space-y-0.5">
                        <Label htmlFor="push_all">Enable All</Label>
                        <p className="text-sm text-muted-foreground">
                          Enable all push notifications
                        </p>
                      </div>
                      <Switch id="push_all" defaultChecked />
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div className="space-y-0.5">
                        <Label htmlFor="push_sound">Sound</Label>
                        <p className="text-sm text-muted-foreground">
                          Play a sound for notifications
                        </p>
                      </div>
                      <Switch id="push_sound" defaultChecked />
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
            <CardFooter className="flex justify-end">
              <Button>Save Preferences</Button>
            </CardFooter>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
} 