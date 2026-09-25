import type { Metadata } from "next"
import { redirect } from "next/navigation"
import Header from "@/app/_components/header"
import { Button } from "@/app/_components/ui/button"
import { Card, CardContent } from "@/app/_components/ui/card"
import { Input } from "@/app/_components/ui/input"
import { testLogin } from "./_actions/test-login"

export const metadata: Metadata = {
  title: "Entrar | Siltec-Barber",
  description: "Entre para agendar e gerenciar seus horários.",
  robots: { index: false, follow: false },
}

interface LoginProps {
  searchParams: Promise<{ erro?: string }>
}

const Login = async ({ searchParams }: LoginProps) => {
  if (process.env.TEST_LOGIN_ENABLED !== "true") {
    redirect("/")
  }

  const { erro } = await searchParams

  return (
    <div className="from-background via-background to-muted/20 min-h-svh bg-linear-to-br">
      <Header />

      <div className="mx-auto max-w-md px-5 py-12 lg:py-16">
        <Card className="border-0 backdrop-blur-sm">
          <CardContent className="space-y-6 p-6 lg:p-8">
            <header className="space-y-2 text-center">
              <h1 className="text-2xl font-bold lg:text-3xl">Entrar</h1>
              <p className="text-muted-foreground text-sm">
                Use seu e-mail e senha para acessar sua conta.
              </p>
            </header>

            {erro && (
              <p role="alert" className="text-destructive text-sm font-medium">
                E-mail ou senha inválidos.
              </p>
            )}

            <form action={testLogin} className="space-y-4">
              <div className="space-y-2">
                <label htmlFor="email" className="text-sm font-medium">
                  E-mail
                </label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  placeholder="voce@exemplo.com"
                  required
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="password" className="text-sm font-medium">
                  Senha
                </label>
                <Input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  placeholder="••••••••"
                  required
                />
              </div>

              <Button type="submit" className="w-full">
                Entrar
              </Button>
            </form>

            <p className="text-muted-foreground text-center text-xs">
              Contas de teste: cliente@teste.dev (cliente), vazio@teste.dev
              (cliente sem reservas) e admin@teste.dev (admin).
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default Login
