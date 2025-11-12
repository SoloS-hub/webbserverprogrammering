-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Värd: 127.0.0.1
-- Tid vid skapande: 23 nov 2023 kl 10:39
-- Serverversion: 10.4.24-MariaDB
-- PHP-version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Databas: `un_global_goals`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/`un_global_goals` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `un_global_goals`;

-- --------------------------------------------------------

--
-- Tabellstruktur `goals`
--

CREATE TABLE `goals` (
  `id` int(11) NOT NULL,
  `name` varchar(300) DEFAULT NULL,
  `description` varchar(2000) NOT NULL,
  `color_code` varchar(6) NOT NULL,
  `short_description` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumpning av Data i tabell `goals`
--

INSERT INTO `goals` (`id`, `name`, `description`, `color_code`, `short_description`) VALUES
(1, 'No Poverty', 'Eradicating poverty is not a task of charity, it’s an act of justice and the key to unlocking an enormous human potential. Still, nearly half of the world’s population lives in poverty, and lack of food and clean water is killing thousands every single day of the year. Together, we can feed the hungry, wipe out disease and give everyone in the world a chance to prosper and live a productive and rich life.', 'e5233b', 'End poverty in all its forms everywhere.'),
(2, 'No hunger', 'Hunger is the leading cause of death in the world. Our planet has provided us with tremendous resources, but unequal access and inefficient handling leaves millions of people malnourished. If we promote sustainable agriculture with modern technologies and fair distribution systems, we can sustain the whole world’s population and make sure that nobody will ever suffer from hunger again.', 'E4B634', 'End hunger, achieve food security and improved nutrition and promote sustainable agriculture.');

-- --------------------------------------------------------

--
-- Tabellstruktur `targets`
--

CREATE TABLE `targets` (
  `id` int(11) NOT NULL,
  `goal_id` int(11) DEFAULT NULL,
  `code` varchar(5) DEFAULT NULL,
  `name` varchar(200) DEFAULT NULL,
  `description` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumpning av Data i tabell `targets`
--

INSERT INTO `targets` (`id`, `goal_id`, `code`, `name`, `description`) VALUES
(1, 1, '1.1', 'Eradicate Extreme Poverty', 'By 2030, eradicate extreme poverty for all people everywhere, currently measured as people living on less than $1.25 a day.'),
(2, 1, '1.2', 'Reduce Poverty by at Least 50%', 'By 2030, reduce at least by half the proportion of men, women and children of all ages living in poverty in all its dimensions according to national definitions.'),
(3, 2, '2.1', 'UNIVERSAL ACCESS TO SAFE AND NUTRITIOUS FOOD ', 'By 2030, end hunger and ensure access by all people, in particular the poor and people in vulnerable situations, including infants, to safe, nutritious and sufficient food all year round.'),
(4, 2, '2.2', 'END ALL FORMS OF MALNUTRITION', 'By 2030, end all forms of malnutrition, including achieving, by 2025, the internationally agreed targets on stunting and wasting in children under 5 years of age, and address the nutritional needs of adolescent girls, pregnant and lactating women and older persons.'),
(5, 2, '2.3', 'DOUBLE THE PRODUCTIVITY AND INCOMES OF SMALL-SCALE FOOD PRODUCERS', 'By 2030, double the agricultural productivity and incomes of small-scale food producers, in particular women, indigenous peoples, family farmers, pastoralists and fishers, including through secure and equal access to land, other productive resources and inputs, knowledge, financial services, markets and opportunities for value addition and non-farm employment.'),
(6, 2, '2.4', 'SUSTAINABLE FOOD PRODUCTION AND RESILIENT AGRICULTURAL PRACTICES', 'By 2030, ensure sustainable food production systems and implement resilient agricultural practices that increase productivity and production, that help maintain ecosystems, that strengthen capacity for adaptation to climate change, extreme weather, drought, flooding and other disasters and that progressively improve land and soil quality.');

--
-- Index för dumpade tabeller
--

--
-- Index för tabell `goals`
--
ALTER TABLE `goals`
  ADD PRIMARY KEY (`id`);

--
-- Index för tabell `targets`
--
ALTER TABLE `targets`
  ADD PRIMARY KEY (`id`),
  ADD KEY `goal_id` (`goal_id`);

--
-- AUTO_INCREMENT för dumpade tabeller
--

--
-- AUTO_INCREMENT för tabell `goals`
--
ALTER TABLE `goals`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT för tabell `targets`
--
ALTER TABLE `targets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Restriktioner för dumpade tabeller
--

--
-- Restriktioner för tabell `targets`
--
ALTER TABLE `targets`
  ADD CONSTRAINT `targets_ibfk_1` FOREIGN KEY (`goal_id`) REFERENCES `goals` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
