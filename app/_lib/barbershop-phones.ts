export const serializePhones = (phones: string[]): string =>
  JSON.stringify(phones)

export const parsePhones = (value: string): string[] => {
  try {
    const parsed: unknown = JSON.parse(value)

    if (!Array.isArray(parsed)) return []

    return parsed.filter((phone): phone is string => typeof phone === "string")
  } catch {
    return []
  }
}
