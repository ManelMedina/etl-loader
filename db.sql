--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: iphistory; Type: DATABASE; Schema: -; Owner: aaron
--

CREATE DATABASE iphistory WITH TEMPLATE = template0 ENCODING = 'SQL_ASCII' LC_COLLATE = 'C' LC_CTYPE = 'C';


ALTER DATABASE iphistory OWNER TO aaron;

\connect iphistory

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: country; Type: TABLE; Schema: public; Owner: aaron; Tablespace: 
--

CREATE TABLE country (
    cc character varying(2) NOT NULL,
    population integer,
    internet_users integer,
    fixed_broadband_subscribers integer,
    ips integer,
    gdp_per_capita_ppp double precision,
    gni_ppp double precision
);


ALTER TABLE country OWNER TO aaron;

--
-- Name: hits; Type: TABLE; Schema: public; Owner: aaron; Tablespace: 
--

CREATE TABLE hits (
    ts timestamp with time zone NOT NULL,
    risk_id integer NOT NULL,
    ip inet NOT NULL,
    "place.cc" character varying(2),
    "place.lat" double precision,
    "place.lon" double precision,
    asn integer
);


ALTER TABLE hits OWNER TO aaron;

--
-- Name: risk; Type: TABLE; Schema: public; Owner: aaron; Tablespace: 
--

CREATE TABLE risk (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE risk OWNER TO aaron;

--
-- Name: risk_id_seq; Type: SEQUENCE; Schema: public; Owner: aaron
--

CREATE SEQUENCE risk_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE risk_id_seq OWNER TO aaron;

--
-- Name: risk_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: aaron
--

ALTER SEQUENCE risk_id_seq OWNED BY risk.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: aaron
--

ALTER TABLE ONLY risk ALTER COLUMN id SET DEFAULT nextval('risk_id_seq'::regclass);


--
-- Name: country_pkey; Type: CONSTRAINT; Schema: public; Owner: aaron; Tablespace: 
--

ALTER TABLE ONLY country
    ADD CONSTRAINT country_pkey PRIMARY KEY (cc);


--
-- Name: risk_pkey; Type: CONSTRAINT; Schema: public; Owner: aaron; Tablespace: 
--

ALTER TABLE ONLY risk
    ADD CONSTRAINT risk_pkey PRIMARY KEY (id);


--
-- Name: hits_risk_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: aaron
--

ALTER TABLE ONLY hits
    ADD CONSTRAINT hits_risk_id_fkey FOREIGN KEY (risk_id) REFERENCES risk(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

