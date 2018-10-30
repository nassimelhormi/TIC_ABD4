-- phpMyAdmin SQL Dump
-- version 4.7.2
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:3306
-- Généré le :  mar. 30 oct. 2018 à 16:25
-- Version du serveur :  5.6.35
-- Version de PHP :  7.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Base de données :  `vdm_db`
--

-- --------------------------------------------------------

--
-- Structure de la table `Clients`
--

CREATE TABLE `Clients` (
  `id_client` int(11) NOT NULL,
  `gender` enum('Monsieur','Madame') NOT NULL,
  `age` int(11) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `first_name` varchar(64) NOT NULL,
  `last_name` varchar(64) NOT NULL,
  `tarif` enum('Plein Tarif','Senior','Etudiant','Junior') NOT NULL,
  `is_acheteur` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `Clients`
--

INSERT INTO `Clients` (`id_client`, `gender`, `age`, `email`, `first_name`, `last_name`, `tarif`, `is_acheteur`) VALUES
(64, 'Monsieur', 64, 'carmine.art@gogole.com', 'Carmine', 'Art', 'Senior', 1),
(63, 'Madame', 22, '', 'Nya', 'Kayla', 'Plein Tarif', 0);

-- --------------------------------------------------------

--
-- Structure de la table `Reservations`
--

CREATE TABLE `Reservations` (
  `id_reservation` int(11) NOT NULL,
  `day` varchar(64) NOT NULL,
  `hour` varchar(64) NOT NULL,
  `is_vr` tinyint(4) NOT NULL DEFAULT '0',
  `g_name` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `Reservations`
--

INSERT INTO `Reservations` (`id_reservation`, `day`, `hour`, `is_vr`, `g_name`) VALUES
(66, '2018-09-07', '05:30', 0, 'Interminable attente chez le medecin');

-- --------------------------------------------------------

--
-- Structure de la table `Spectateurs`
--

CREATE TABLE `Spectateurs` (
  `id_client` int(11) NOT NULL,
  `id_reservation` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `Spectateurs`
--

INSERT INTO `Spectateurs` (`id_client`, `id_reservation`) VALUES
(63, 66),
(64, 66);

-- --------------------------------------------------------

--
-- Structure de la table `Users`
--

CREATE TABLE `Users` (
  `id_user` int(11) NOT NULL,
  `username` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `Clients`
--
ALTER TABLE `Clients`
  ADD PRIMARY KEY (`id_client`),
  ADD UNIQUE KEY `gender` (`gender`,`age`,`email`,`first_name`,`last_name`,`tarif`,`is_acheteur`);

--
-- Index pour la table `Reservations`
--
ALTER TABLE `Reservations`
  ADD PRIMARY KEY (`id_reservation`);

--
-- Index pour la table `Spectateurs`
--
ALTER TABLE `Spectateurs`
  ADD KEY `id_client` (`id_client`,`id_reservation`),
  ADD KEY `fdx_res` (`id_reservation`);

--
-- Index pour la table `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `Clients`
--
ALTER TABLE `Clients`
  MODIFY `id_client` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;
--
-- AUTO_INCREMENT pour la table `Reservations`
--
ALTER TABLE `Reservations`
  MODIFY `id_reservation` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=67;
--
-- AUTO_INCREMENT pour la table `Users`
--
ALTER TABLE `Users`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT;
--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `Spectateurs`
--
ALTER TABLE `Spectateurs`
  ADD CONSTRAINT `fdx_res` FOREIGN KEY (`id_reservation`) REFERENCES `Reservations` (`id_reservation`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fdx_spec` FOREIGN KEY (`id_client`) REFERENCES `Clients` (`id_client`) ON DELETE NO ACTION ON UPDATE NO ACTION;
