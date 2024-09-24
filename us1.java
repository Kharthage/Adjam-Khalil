import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet, ActivityIndicator } from 'react-native';

const MatchsPage = () => {
  const [matchs, setMatchs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Appel à l'API pour récupérer les données des matchs auxquels l'utilisateur a parié
    const fetchMatchs = async () => {
      try {
        const response = await fetch('https://votre-api.com/matchs-paries');
        if (!response.ok) {
          throw new Error('Erreur lors de la récupération des matchs');
        }
        const data = await response.json();
        setMatchs(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchMatchs();
  }, []);

  const renderItem = ({ item }) => (
    <View style={[styles.matchItem, item.statut !== 'En Cours' ? styles.matchGrise : null]}>
      <Text style={styles.teamNames}>Nom des équipes : {item.equipes}</Text>
      <Text>Date de début : {item.date_debut}</Text>
      <Text>Date de fin : {item.date_fin}</Text>
      {item.statut === 'Terminé' && <Text>Score : {item.score}</Text>}
    </View>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#0000ff" />
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>{error}</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={matchs}
        renderItem={renderItem}
        keyExtractor={item => item.id.toString()}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 10,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  errorText: {
    color: 'red',
    fontSize: 16,
  },
  matchItem: {
    padding: 10,
    marginBottom: 10,
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
  },
  matchGrise: {
    backgroundColor: '#f9f9f9',
    color: '#bbb',
  },
  teamNames: {
    fontWeight: 'bold',
  },
});

export default MatchsPage;
