import type { Metadata, Viewport } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import { Toaster } from "./_components/ui/sonner"
import AuthProvider from "./_providers/auth"
import ProgressProvider from "./_components/progress-bar"
import DemoBanner from "./_components/demo-banner"
import { SpeedInsights } from "@vercel/speed-insights/next"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  metadataBase: new URL("https://barber-lab.vercel.app/"),
  title: "Siltec-Barber - Sistema para Barbearias | Agendamento Online",
  description:
    "Siltec-Barber é o sistema ideal para barbearias. Agende horários online, encontre barbearias próximas e gerencie seus agendamentos facilmente.",
  keywords: [
    "Siltec-Barber",
    "sistema para barbearia",
    "agendamento barbearia",
    "barbearia online",
    "software barbearia",
    "agendar corte de cabelo",
    "barbearias próximas",
    "Barbearia",
    "Cabeleireiro",
    "siltec-barber",
  ],
  openGraph: {
    title: "Siltec-Barber - Sistema para Barbearia",
    description:
      "Encontre e agende nas melhores barbearias com o Siltec-Barber. Plataforma completa para clientes e barbeiros.",
    url: "https://barber-lab.vercel.app/",
    siteName: "Siltec-Barber",
    images: [
      {
        url: "/mobile-banner.png",
        width: 1200,
        height: 630,
        alt: "Siltec-Barber - Sistema para Barbearia",
      },
    ],
    locale: "pt_BR",
    type: "website",
  },
}

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
  themeColor: "#151619",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="pt-br" className="dark">
      <body className={inter.className}>
        <DemoBanner />
        <AuthProvider>
          <ProgressProvider>{children}</ProgressProvider>
        </AuthProvider>
        <Toaster />
        <SpeedInsights />
      </body>
    </html>
  )
}
