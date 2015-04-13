# Name: Steven Bradley
# CSE 140
# Homework 4

import networkx as nx
import matplotlib.pyplot as plt
import operator
from operator import itemgetter, attrgetter
import random


###
### Problem 1a
###

practice_graph = nx.Graph()

# create nodes
practice_graph.add_node("A")
practice_graph.add_node("B")
practice_graph.add_node("C")
practice_graph.add_node("D")
practice_graph.add_node("E")
practice_graph.add_node("F")

# create edges between nodes
practice_graph.add_edge("A", "B")
practice_graph.add_edge("A", "C")
practice_graph.add_edge("B", "C")
practice_graph.add_edge("B", "D")
practice_graph.add_edge("C", "D")
practice_graph.add_edge("C", "F")
practice_graph.add_edge("D", "F")
practice_graph.add_edge("E", "D")

assert len(practice_graph.nodes()) == 6
assert len(practice_graph.edges()) == 8

def draw_practice_graph():
    """Draw practice_graph to the screen."""
    nx.draw(practice_graph)
    plt.show()

# Comment out this line after you have visually verified your practice graph.
# Otherwise, the picture will pop up every time that you run your program.
# draw_practice_graph()


###
### Problem 1b
###

rj = nx.Graph()

# create nodes
rj.add_node("Romeo")
rj.add_node("Benvolio")
rj.add_node("Montague")
rj.add_node("Juliet")
rj.add_node("Tybalt")
rj.add_node("Capulet")
rj.add_node("Escalus")
rj.add_node("Mercutio")
rj.add_node("Paris")
rj.add_node("Nurse")
rj.add_node("Friar Laurence")

# create edges between nodes
rj.add_edge("Romeo", "Benvolio")
rj.add_edge("Romeo", "Juliet")
rj.add_edge("Romeo", "Montague")
rj.add_edge("Romeo", "Friar Laurence")
rj.add_edge("Romeo", "Mercutio")
rj.add_edge("Montague", "Benvolio")
rj.add_edge("Montague", "Escalus")
rj.add_edge("Juliet", "Tybalt")
rj.add_edge("Juliet", "Nurse")
rj.add_edge("Juliet", "Capulet")
rj.add_edge("Juliet", "Romeo")
rj.add_edge("Juliet", "Friar Laurence")
rj.add_edge("Capulet", "Tybalt")
rj.add_edge("Capulet", "Escalus")
rj.add_edge("Capulet", "Paris")
rj.add_edge("Escalus", "Mercutio")
rj.add_edge("Paris", "Escalus")
rj.add_edge("Paris", "Mercutio")

assert len(rj.nodes()) == 11
assert len(rj.edges()) == 17

def draw_rj():
    """Draw the rj graph to the screen and to a file."""
    nx.draw(rj)
    plt.savefig("romeo-and-juliet.pdf")
    plt.show()

# Comment out this line after you have visually verified your rj graph and
# created your PDF file.
# Otherwise, the picture will pop up every time that you run your program.
#draw_rj()


###
### Problem 2
###

def friends(graph, user):
    """Returns a set of the friends of the given user, in the given graph.
    The parameter 'user' is the string name of a person in the graph.
    """
    return set(graph.neighbors(user))


def friends_of_friends(graph, user):
    """Returns a set of friends of friends of the given user, in the given graph.
    The result does not include the given user nor any of that user's friends.
    """
    result = set();
    friends = graph.neighbors(user);
    for friend in friends:
        friends_of_friend = graph.neighbors(friend);
        for pal in friends_of_friend:
            result.add(pal);
    for friend in friends:
        # friends of friends doesn't include a users direct friends
        if friend in result:
            result.remove(friend);
    result.remove(user);
    return result;

assert friends_of_friends(rj, "Mercutio") == set(['Benvolio', 'Capulet', 'Friar Laurence', 'Juliet', 'Montague'])


def common_friends(graph, user1, user2):
    """Returns the set of friends that user1 and user2 have in common."""
    friends1 = set(graph.neighbors(user1));
    friends2 = set(graph.neighbors(user2));
    return friends1 & friends2;

assert common_friends(practice_graph,"A", "B") == set(['C'])
assert common_friends(practice_graph,"A", "D") == set(['B', 'C'])
assert common_friends(practice_graph,"A", "E") == set([])
assert common_friends(practice_graph,"A", "F") == set(['C'])

assert common_friends(rj, "Mercutio", "Nurse") == set()
assert common_friends(rj, "Mercutio", "Romeo") == set()
assert common_friends(rj, "Mercutio", "Juliet") == set(["Romeo"])
assert common_friends(rj, "Mercutio", "Capulet") == set(["Escalus", "Paris"])


def number_of_common_friends_map(graph, user):
    """Returns a map from each user U to the number of friends U has in common with the given user.
    The map only contains users who have at least one friend in common with U,
    and are neither U nor one of U's friends.
    Take a graph G for example: 
        - A and B have two friends in common
        - A and C have one friend in common
        - A and D have one friend in common
        - A and E have no friends in common
        - A is friends with D
    number_of_common_friends_map(G, "A")  =>   { 'B':2, 'C':1 }
    """
    num_common = dict();
    network = graph.nodes();
    network.remove(user);
    for person in network:
        common = common_friends(graph, user, person);
        for friend in common:
            # ensures that common friends dont get counted twice
            if (len(common) > 0 and (person not in graph.neighbors(user))):
                num_common[person] = len(common);
    return num_common;
        
assert number_of_common_friends_map(practice_graph, "A") == {'D': 2, 'F': 1}

assert number_of_common_friends_map(rj, "Mercutio") == { 'Benvolio': 1, 'Capulet': 2, 'Friar Laurence': 1, 'Juliet': 1, 'Montague': 2 }


def number_map_to_sorted_list(map):
    """Given a map whose values are numbers, return a list of the keys.
    The keys are sorted by the number they map to, from greatest to least.
    When two keys map to the same number, the keys are sorted by their
    natural sort order, from least to greatest."""
    lst = [];
    for key in map:
        lst.append([key, -map[key]]);
    # sorts by value then by key
    lst = sorted(lst, key=itemgetter(1,0));
    for person in lst:
        result = [person[0] for person in lst];
    return result;

assert number_map_to_sorted_list({"a":5, "b":2, "c":7, "d":5, "e":5}) == ['c', 'a', 'd', 'e', 'b']


def recommend_by_number_of_common_friends(graph, user):
    """Return a list of friend recommendations for the given user.
    The friend recommendation list consists of names of people in the graph
    who are not yet a friend of the given user.
    The order of the list is determined by the number of common friends. 
    """
    common_friends = number_of_common_friends_map(graph, user);
    return number_map_to_sorted_list(common_friends);
    
assert recommend_by_number_of_common_friends(practice_graph,"A") == ['D', 'F']

assert recommend_by_number_of_common_friends(rj, "Mercutio") == ['Capulet', 'Montague', 'Benvolio', 'Friar Laurence', 'Juliet']


###
### Problem 3
###

def influence_map(graph, user):
    """Returns a map from each user U to the friend influence, with respect to the given user.
    The map only contains users who have at least one friend in common with U,
    and are neither U nor one of U's friends.
    See the assignment for the definition of friend influence.
    """
    influences = dict();
    friends_of = friends_of_friends(graph, user);
    for friend in friends_of:
        influences[friend] = 0;
        com = common_friends(graph, user, friend);
        for person in com:
            influences[friend] += 1.0/len(friends(graph, person));
    return influences;

assert influence_map(rj,"Mercutio") =={ 'Benvolio': 0.2,'Capulet': 0.5833333333333333,'Friar Laurence': 0.2,'Juliet': 0.2,'Montague': 0.45 }


def recommend_by_influence(graph, user):
    """Return a list of friend recommendations for the given user.
    The friend recommendation list consists of names of people in the graph
    who are not yet a friend of the given user.
    The order of the list is determined by the influence measurement.
    """
    influences = influence_map(graph, user);
    return number_map_to_sorted_list(influences);

assert recommend_by_influence(rj, "Mercutio") == ['Capulet', 'Montague', 'Benvolio', 'Friar Laurence', 'Juliet']


###
### Problem 4
###
def compare_recommendations(graph, user):
    """Returns True if the two recommendation systems gave the same
    exact recommendations for the given user in the given graph.
    Otherwise returns False
    """
    rec1 = recommend_by_influence(graph,user);
    rec2 = recommend_by_number_of_common_friends(graph, user);
    return  rec1 == rec2;

def print_results(graph):
    """Prints two lists for the given graph. One for the users that get the same recommendation
    from both recommendation systems, and one for the users that get
    different recommendations.
    """
    same = [];
    dif = [];
    nodes = graph.nodes();
    for node in nodes:
        if(compare_recommendations(graph, node)):
            same.append(node);
        else:
            dif.append(node);
    print "Unchanged recommendations:", sorted(same);
    print "Changed recommendations:", sorted(dif);

print_results(rj);


###
### Problem 5
###

# (There is no code to write for this problem.)


###
### Problem 6
###

# (There is no code to write for this problem.)


###
### Problem 7
###
def test_recommendation_systems(graph):
    """Compares the effectiveness of the influence and common method
    recommendation systems. Two random friends are chosen, and then
    the recommendation methods are run on them to determine which
    recommends the friend first(This gives the rank). Prints the average
    rank of each method and prints out the results.
    """
    # used to keep track of index sums
    indx_inf = 0;
    indx_com = 0;
    # count of indexes to average
    inf_count = 0;
    com_count = 0;
    for i in range(100):  
        #pick random two friends f1, f2
        f1 = random.choice(list(graph.nodes()));
        f1_friends = list(friends(graph, f1));
        f2 = random.choice(list(friends(graph, f1)));
        f2_friends = list(friends(graph, f2));
        graph.remove_edge(f1,f2);
        if(f1_friends != [f2]):
            #test influence method
            if (f2_friends != []):
                inf_lst = recommend_by_influence(graph,f1);
                if f2 in inf_lst:
                    indx_inf += inf_lst.index(f2) + 1;
                    inf_count += 1;
                #test common method
                com_lst = recommend_by_number_of_common_friends(graph,f1);
                if f2 in com_lst:
                    indx_com += com_lst.index(f2) + 1;
                    com_count += 1;
        if(f2_friends != [f1]):
            #test influence method
            if (f2_friends != [f1]):
                inf_lst = recommend_by_influence(graph,f2);
                if f1 in inf_lst:
                    indx_inf += inf_lst.index(f1) + 1;
                    inf_count += 1;
                #test common method
                com_lst = recommend_by_number_of_common_friends(graph,f2);
                if f1 in com_lst:
                    indx_com += com_lst.index(f1) + 1;
                    com_count += 1;
        graph.add_edge(f1,f2);

    #computer averages
    inf_avg = float(indx_inf)/inf_count;
    com_avg = float(indx_com)/com_count;

    #print results
    print "Average rank of influence method:", inf_avg;
    print "Average rank of number of friends in common method:", com_avg;
    if(inf_avg < com_avg):
        print "The influence method is better.";
    elif(com_avg < inf_avg):
        print "The number of friends in common method is better.";
    else:
        print "Both methods are equal in this case.";

test_recommendation_systems(rj);
    

###
### Problem 8
###
fb_data = open("facebook-links.txt");
facebook = nx.Graph();
for line in fb_data:
    info = line.split('\t');
    facebook.add_node(info[0]);
    facebook.add_node(info[1]);
    facebook.add_edge(info[0], info[1]);

assert len(facebook.nodes()) == 63731
assert len(facebook.edges()) == 817090


###
### Problem 9
###
users = sorted(facebook.nodes(), key=float);
for user in users:
    if float(user) % 1000 == 0:
        recs = recommend_by_number_of_common_friends(facebook, user);
        fst_ten = [];
        if len(recs) >= 10:
            for i in range(10):
                fst_ten.append(recs[i]);
        else:
            fst_ten = recs;
        print user, fst_ten;

###
### Problem 10
###
users = sorted(facebook.nodes(), key=float);
for user in users:
    if float(user) % 1000 == 0:
        recs = recommend_by_influence(facebook, user);
        fst_ten = [];
        if len(recs) >= 10:
            for i in range(10):
                fst_ten.append(recs[i]);
        else:
            fst_ten = recs;
        print user, fst_ten;

###
### Problem 11
###
        
users = sorted(facebook.nodes(), key=float);
same_count = 0;
dif_count = 0;
for user in users:
    if float(user) % 1000 == 0:
        inf_recs = recommend_by_influence(facebook, user);
        com_recs = recommend_by_number_of_common_friends(facebook, user);
        inf_ten = [];
        com_ten = [];
        if len(inf_recs) >= 10:
            for i in range(10):
                inf_ten.append(inf_recs[i]);
        else:
            inf_ten = recs;
        if len(com_recs) >= 10:
            for i in range(10):
                com_ten.append(com_recs[i]);
        else:
            com_ten = com_recs;
        if inf_ten == com_ten:
            same_count += 1;
        else:
            dif_count += 1;
print "Same:", str(same_count)+",", "Different:", dif_count;

###
### Problem 12
###

test_recommendation_systems(facebook);

