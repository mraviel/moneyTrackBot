--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5 (Ubuntu 14.5-1.pgdg20.04+1)
-- Dumped by pg_dump version 14.5 (Ubuntu 14.5-1.pgdg20.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: messages; Type: TABLE; Schema: public; Owner: user1
--

CREATE TABLE public.messages (
    message_id integer NOT NULL,
    author_id integer NOT NULL,
    is_expense boolean NOT NULL,
    message_datetime timestamp NOT NULL,
    subject character varying(20) NOT NULL,
    total numeric NOT NULL
);


ALTER TABLE public.messages OWNER TO user1;

--
-- Name: subjects; Type: TABLE; Schema: public; Owner: user1
--

CREATE TABLE public.subjects (
    id integer NOT NULL,
    author_id integer NOT NULL,
    subjectד_title character varying(20) NOT NULL
);


ALTER TABLE public.subjects OWNER TO user1;

--
-- Name: subjects_id_seq; Type: SEQUENCE; Schema: public; Owner: user1
--

CREATE SEQUENCE public.subjects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subjects_id_seq OWNER TO user1;

--
-- Name: subjects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user1
--

ALTER SEQUENCE public.subjects_id_seq OWNED BY public.subjects.id;


--
-- Name: subjects id; Type: DEFAULT; Schema: public; Owner: user1
--

ALTER TABLE ONLY public.subjects ALTER COLUMN id SET DEFAULT nextval('public.subjects_id_seq
'::regclass);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: user1
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (message_id);


--
-- Name: subjects subjects_pkey; Type: CONSTRAINT; Schema: public; Owner: user1
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT subjects_pkey PRIMARY KEY (id);


--
-- Name: subjects unique_subjects; Type: CONSTRAINT; Schema: public; Owner: user1
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT unique_subjects UNIQUE (author_id, subject_title);


--
-- PostgreSQL database dump complete
--