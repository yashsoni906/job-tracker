export type ApplicationStatus = "applied" | "interview" | "offer" | "rejected";

export interface Application {
  id: number;
  company_id: number;
  contact_id: number | null;
  role_title: string;
  status: ApplicationStatus;
  date_applied: string;
  date_updated: string;
  source: string | null;
  notes: string | null;
  url: string | null;
}