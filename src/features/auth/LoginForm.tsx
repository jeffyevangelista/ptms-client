import { Button } from "@/components/ui/button";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useLogin } from "./auth.hooks";
import { useState } from "react";
import { CircleX, Loader } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

const LoginForm = () => {
  const { isPending, isError, error, mutateAsync: login } = useLogin();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    await login({ email, password });
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>Login to your account</CardTitle>
        <CardDescription>
          Enter your email below to login to your account
        </CardDescription>
      </CardHeader>

      <CardContent>
        <form onSubmit={handleLogin}>
          <div className="flex flex-col gap-6">
            {isError && (
              <Alert variant="destructive">
                <CircleX />
                <AlertTitle>Oops!</AlertTitle>
                <AlertDescription>{error.message}</AlertDescription>
              </Alert>
            )}
            <div className="grid gap-3">
              <Label htmlFor="email">Email</Label>
              <Input
                required
                disabled={isPending}
                id="email"
                type="email"
                value={email}
                onChange={({ target }) => setEmail(target.value)}
                placeholder="m@example.com"
              />
            </div>
            <div className="grid gap-3">
              <div className="flex items-center">
                <Label htmlFor="password">Password</Label>
                <a
                  href="#"
                  className="ml-auto inline-block text-sm underline-offset-4 hover:underline"
                >
                  Forgot your password?
                </a>
              </div>
              <Input
                required
                disabled={isPending}
                value={password}
                onChange={({ target }) => setPassword(target.value)}
                id="password"
                type="password"
              />
            </div>

            <Button type="submit" disabled={isPending} className="w-full">
              {isPending && <Loader className="animate-spin" />}
              Login
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
};

export default LoginForm;
