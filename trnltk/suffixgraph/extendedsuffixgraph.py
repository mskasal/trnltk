# coding=utf-8
from trnltk.stem.dictionaryitem import RootAttribute, PrimaryPosition
from trnltk.suffixgraph.suffixconditions import comes_after, followed_by, applies_to_stem, doesnt_come_after, doesnt, followed_by_suffix, that_goes_to, requires_root_attribute, doesnt_come_after_derivation, followed_by_derivation, followed_by_one_from_group
from trnltk.suffixgraph.suffixgraph import SuffixGraph
from trnltk.suffixgraph.suffixgraphmodel import *

class ExtendedSuffixGraph(SuffixGraph):

    def __init__(self):
        SuffixGraph.__init__(self)

        self._add_states()
        self._add_suffixes()
        self._register_suffixes()

    def _add_states(self):
        SuffixGraph._add_states(self)

        self.ALL_STATES.extend({

        })

    def get_default_stem_state(self, stem):
        if not stem.dictionary_item.primary_position or stem.dictionary_item.primary_position==PrimaryPosition.NOUN:
            return self.NOUN_ROOT
        elif stem.dictionary_item.primary_position==PrimaryPosition.VERB:
            return self.VERB_ROOT
        elif stem.dictionary_item.primary_position==PrimaryPosition.ADVERB:
            return self.ADVERB_ROOT
        elif stem.dictionary_item.primary_position==PrimaryPosition.ADJECTIVE:
            return self.ADJECTIVE_ROOT
        elif stem.dictionary_item.primary_position==PrimaryPosition.PRONOUN:
            return self.PRONOUN_ROOT
        elif stem.dictionary_item.primary_position==PrimaryPosition.DETERMINER:
            return self.DETERMINER_ROOT_TERMINAL
        elif stem.dictionary_item.primary_position==PrimaryPosition.INTERJECTION:
            return self.INTERJECTION_ROOT_TERMINAL
        elif stem.dictionary_item.primary_position==PrimaryPosition.CONJUNCTION:
            return self.CONJUNCTION_ROOT_TERMINAL
        elif stem.dictionary_item.primary_position==PrimaryPosition.NUMERAL:
            return self.NUMERAL_ROOT
        elif stem.dictionary_item.primary_position==PrimaryPosition.PUNCTUATION:
            return self.PUNC_ROOT_TERMINAL
        elif stem.dictionary_item.primary_position==PrimaryPosition.PARTICLE:
            return self.PART_ROOT_TERMINAL
        else:
            raise Exception("No stem state found for stem {} !".format(stem))

    def _add_suffixes(self):

        #############  Empty transitions
        FreeTransitionSuffix("Noun_Free_Transition_1",       self.NOUN_WITH_CASE,       self.NOUN_TERMINAL_DERIV)
        FreeTransitionSuffix("Noun_Free_Transition_2",       self.NOUN_WITH_CASE,       self.NOUN_DERIV_WITH_CASE)
        FreeTransitionSuffix("Verb_Free_Transition_1",       self.VERB_ROOT,            self.VERB_PLAIN_DERIV)
        FreeTransitionSuffix("Verb_Free_Transition_2",       self.VERB_WITH_POLARITY,   self.VERB_POLARITY_DERIV)
        FreeTransitionSuffix("Verb_Free_Transition_3",       self.VERB_WITH_TENSE,      self.VERB_TENSE_DERIV)
        FreeTransitionSuffix("Adj_Free_Transition_1",        self.ADJECTIVE_ROOT,       self.ADJECTIVE_TERMINAL)
        FreeTransitionSuffix("Adj_Free_Transition_2",        self.ADJECTIVE_ROOT,       self.ADJECTIVE_DERIV)
        FreeTransitionSuffix("Adv_Free_Transition",          self.ADVERB_ROOT,          self.ADVERB_TERMINAL)
        FreeTransitionSuffix("Pronoun_Free_Transition",      self.PRONOUN_WITH_CASE,    self.PRONOUN_TERMINAL)
        FreeTransitionSuffix("Numeral_Free_Transition",      self.NUMERAL_ROOT,         self.NUMERAL_DERIV)

        ZeroTransitionSuffix("Numeral_Zero_Transition",      self.NUMERAL_DERIV,        self.ADJECTIVE_ROOT)
        ZeroTransitionSuffix("Noun_to_Verb_Zero_Transition", self.NOUN_DERIV_WITH_CASE, self.VERB_FROM_OTHER_POS)
        ZeroTransitionSuffix("Adj_to_Noun_Zero_Transition",  self.ADJECTIVE_DERIV,      self.NOUN_ROOT)
        ZeroTransitionSuffix("Verb_to_Adj_Zero_Transition",  self.VERB_TENSE_ADJ_DERIV, self.ADJECTIVE_ROOT)

        #TODO: transition from numeral to adverb for case "birer birer geldiler?" hmm maybe duplication caused an adj->adv transition?

        #############  Noun Agreements
        self.Noun_Agreements_Group = SuffixGroup("Noun_Agreements_Group")
        self.A3Sg_Noun = Suffix("A3Sg_Noun", self.Noun_Agreements_Group, 'A3sg')
        self.A3Pl_Noun = Suffix("A3Pl_Noun", self.Noun_Agreements_Group, 'A3pl')

        ###########  Possessive agreements
        self.Noun_Possessions_Group = SuffixGroup("Noun_Possession_Group")
        self.Pnon_Noun = Suffix("Pnon_Noun", self.Noun_Possessions_Group, "Pnon")
        self.P1Sg_Noun = Suffix("P1sg_Noun", self.Noun_Possessions_Group, "P1sg")
        self.P2Sg_Noun = Suffix("P2sg_Noun", self.Noun_Possessions_Group, "P2sg")
        self.P3Sg_Noun = Suffix("P3sg_Noun", self.Noun_Possessions_Group, "P3sg")
        self.P1Pl_Noun = Suffix("P1pl_Noun", self.Noun_Possessions_Group, "P1pl")
        self.P2Pl_Noun = Suffix("P2pl_Noun", self.Noun_Possessions_Group, "P2pl")
        self.P3Pl_Noun = Suffix("P3pl_Noun", self.Noun_Possessions_Group, "P3pl")

        ###########  Noun cases
        self.Noun_Cases_Group = SuffixGroup('Noun_Case_Group')
        self.Nom_Noun = Suffix("Nom_Noun", self.Noun_Cases_Group, "Nom")
        self.Nom_Noun_Deriv = Suffix("Nom_Deriv_Noun", self.Noun_Cases_Group, "Nom")
        self.Acc_Noun = Suffix("Acc_Noun", self.Noun_Cases_Group, "Acc")
        self.Dat_Noun = Suffix("Dat_Noun", self.Noun_Cases_Group, "Dat")
        self.Loc_Noun = Suffix("Loc_Noun", self.Noun_Cases_Group, "Loc")
        self.Abl_Noun = Suffix("Abl_Noun", self.Noun_Cases_Group, "Abl")

        self.Gen_Noun = Suffix("Gen_Noun", self.Noun_Cases_Group, "Gen")
        self.Ins_Noun = Suffix("Ins_Noun", self.Noun_Cases_Group, "Ins")

        ############# Noun to Noun derivations
        self.Agt_Noun = Suffix("Agt_Noun", pretty_name='Agt')
        self.Dim = Suffix("Dim")

        ############# Noun to Verb derivations
        self.Acquire = Suffix("Acquire")

        ############# Noun to Adjective derivations
        self.With = Suffix("With")
        self.Without = Suffix("Without")
        self.Rel = Suffix("Rel")

        ############# Verb agreements
        self.Verb_Agreements_Group = SuffixGroup('Verb_Agreements_Group')
        self.A1Sg_Verb = Suffix("A1Sg_Verb", self.Verb_Agreements_Group, "A1sg")
        self.A2Sg_Verb = Suffix("A2Sg_Verb", self.Verb_Agreements_Group, "A2sg")
        self.A3Sg_Verb = Suffix("A3Sg_Verb", self.Verb_Agreements_Group, "A3sg")
        self.A1Pl_Verb = Suffix("A1Pl_Verb", self.Verb_Agreements_Group, "A1pl")
        self.A2Pl_Verb = Suffix("A2Pl_Verb", self.Verb_Agreements_Group, "A2pl")
        self.A3Pl_Verb = Suffix("A3Pl_Verb", self.Verb_Agreements_Group, "A3pl")

        ############# Verb from other position agreements
        self.Verb_From_Other_Positions_Agreements_Group = SuffixGroup('Verb_From_Other_Positions_Agreements_Group')
        self.A1Sg_Verb_From_Other_Pos = Suffix("A1Sg_Verb_From_Other_Pos", self.Verb_From_Other_Positions_Agreements_Group, "A1sg")
        self.A2Sg_Verb_From_Other_Pos = Suffix("A2Sg_Verb_From_Other_Pos", self.Verb_From_Other_Positions_Agreements_Group, "A2sg")
        self.A3Sg_Verb_From_Other_Pos = Suffix("A3Sg_Verb_From_Other_Pos", self.Verb_From_Other_Positions_Agreements_Group, "A3sg")
        self.A1Pl_Verb_From_Other_Pos = Suffix("A1Pl_Verb_From_Other_Pos", self.Verb_From_Other_Positions_Agreements_Group, "A1pl")
        self.A2Pl_Verb_From_Other_Pos = Suffix("A2Pl_Verb_From_Other_Pos", self.Verb_From_Other_Positions_Agreements_Group, "A2pl")
        self.A3Pl_Verb_From_Other_Pos = Suffix("A3Pl_Verb_From_Other_Pos", self.Verb_From_Other_Positions_Agreements_Group, "A3pl")

        ############# Verb conditions
        self.Verb_Polarity_Group = SuffixGroup("Verb_Conditions_Group")
        self.Negative = Suffix("Neg", self.Verb_Polarity_Group)
        self.Positive = Suffix("Pos", self.Verb_Polarity_Group)

        ############# Verbal tenses
        self.Aorist = Suffix("Aor")
        self.Progressive = Suffix("Prog")
        self.Future = Suffix("Fut")
        self.Narr = Suffix("Narr")
        self.Past = Suffix("Past")
        self.Pres = Suffix("Pres")

        self.Cond = Suffix("Cond")
        self.Imp = Suffix("Imp")

        ############ Modals
        self.Neces = Suffix("Neces")
        self.Opt = Suffix("Opt")

        ############ Verb to Noun derivations
        self.Inf = Suffix("Inf")
        self.PastPart_Noun = Suffix("PastPart_Noun", pretty_name='PastPart')
        self.FutPart_Noun = Suffix('FutPart_Noun', pretty_name='FutPart')

        ############ Verb to Verb derivations
        self.Able = Suffix("Able")
        self.Pass = Suffix("Pass")
        self.Recip = Suffix("Recip")
        self.Caus = Suffix("Caus", allow_repetition=True)
        self.Hastily = Suffix("Hastily")

        ########### Verb to Adverb derivations
        self.AfterDoingSo = Suffix("AfterDoingSo")
        self.AsLongAs = Suffix("AsLongAs")
        self.ByDoingSo = Suffix("ByDoingSo")
        self.While = Suffix("While")
        self.AsIf = Suffix("AsIf")

        ########### Verb to Adjective derivations
        self.PresPart = Suffix("PresPart")
        self.PastPart_Adj = Suffix("PastPart_Adj", pretty_name='PastPart')
        self.FutPart_Adj = Suffix('FutPart_Adj', pretty_name='FutPart')
        self.Agt_Adj = Suffix('Agt_Adj', pretty_name='Agt')

        self.Aorist_to_Adj = Suffix("Aorist_to_Adj", pretty_name="Aor")
        self.Future_to_Adj = Suffix("Future_to_Adj", pretty_name="Fut")
        self.Narr_to_Adj = Suffix("Narr_to_Adj", pretty_name="Narr")

        ########### Adjective to Adverb derivations
        self.Ly = Suffix("Ly")

        ########### Adjective to Noun derivations
        self.Ness = Suffix("Ness")

        ########### Adjective to Verb derivations
        self.Become = Suffix("Become")

        ########### Adjective possessions
        self.Adjective_Possessions_Group = SuffixGroup("Adjective_Possessions_Group")
        self.Pnon_Adj = Suffix("Pnon_Adj", self.Adjective_Possessions_Group, 'Pnon')
        self.P1Sg_Adj = Suffix("P1Sg_Adj", self.Adjective_Possessions_Group, 'P1sg')
        self.P2Sg_Adj = Suffix("P2Sg_Adj", self.Adjective_Possessions_Group, 'P2sg')
        self.P3Sg_Adj = Suffix("P3Sg_Adj", self.Adjective_Possessions_Group, 'P3sg')
        self.P1Pl_Adj = Suffix("P1Pl_Adj", self.Adjective_Possessions_Group, 'P1pl')
        self.P2Pl_Adj = Suffix("P2Pl_Adj", self.Adjective_Possessions_Group, 'P2pl')
        self.P3Pl_Adj = Suffix("P3Pl_Adj", self.Adjective_Possessions_Group, 'P3pl')

        #############  Pronoun Agreements
        self.Pronoun_Agreements_Group = SuffixGroup("Pronoun_Agreements_Group")
        self.A1Sg_Pron = Suffix("A1Sg_Pron", self.Pronoun_Agreements_Group, 'A1sg')
        self.A2Sg_Pron = Suffix("A2Sg_Pron", self.Pronoun_Agreements_Group, 'A2sg')
        self.A3Sg_Pron = Suffix("A3Sg_Pron", self.Pronoun_Agreements_Group, 'A3sg')
        self.A1Pl_Pron = Suffix("A1Pl_Pron", self.Pronoun_Agreements_Group, 'A1pl')
        self.A2Pl_Pron = Suffix("A2Pl_Pron", self.Pronoun_Agreements_Group, 'A2pl')
        self.A3Pl_Pron = Suffix("A3Pl_Pron", self.Pronoun_Agreements_Group, 'A3pl')

        ########### Pronoun possessions
        self.Pronoun_Possessions_Group = SuffixGroup("Pronoun_Possessions_Group")
        self.Pnon_Pron = Suffix("Pnon_Pron", self.Pronoun_Possessions_Group, 'Pnon')
        self.P1Sg_Pron = Suffix("P1Sg_Pron", self.Pronoun_Possessions_Group, 'P1sg')
        self.P2Sg_Pron = Suffix("P2Sg_Pron", self.Pronoun_Possessions_Group, 'P2sg')
        self.P3Sg_Pron = Suffix("P3Sg_Pron", self.Pronoun_Possessions_Group, 'P3sg')
        self.P1Pl_Pron = Suffix("P1Pl_Pron", self.Pronoun_Possessions_Group, 'P1pl')
        self.P2Pl_Pron = Suffix("P2Pl_Pron", self.Pronoun_Possessions_Group, 'P2pl')
        self.P3Pl_Pron = Suffix("P3Pl_Pron", self.Pronoun_Possessions_Group, 'P3pl')

        ###########  Pronoun cases
        self.Pronoun_Case_Group = SuffixGroup('Pronoun_Case_Group')
        self.Nom_Pron = Suffix("Nom", self.Pronoun_Case_Group)
        self.Nom_Pron_Deriv = Suffix("Nom_Pron_Deriv", self.Pronoun_Case_Group, pretty_name="Nom")
        self.Acc_Pron = Suffix("Acc", self.Pronoun_Case_Group)
        self.Dat_Pron = Suffix("Dat", self.Pronoun_Case_Group)
        self.Loc_Pron = Suffix("Loc", self.Pronoun_Case_Group)
        self.Abl_Pron = Suffix("Abl", self.Pronoun_Case_Group)

        ############# Pronoun case-likes
        self.Gen_Pron = Suffix("Gen", self.Pronoun_Case_Group)
        self.Ins_Pron = Suffix("Ins", self.Pronoun_Case_Group)

        ############# Pronoun to Adjective derivations
        self.Without_Pron = Suffix("Without_Pron", pretty_name="Without")

    def _register_suffixes(self):
        self._register_noun_suffixes()
        self._register_verb_suffixes()
        self._register_adjective_suffixes()
        self._register_pronoun_suffixes()

    def _register_noun_suffixes(self):
        self._register_noun_agreements()
        self._register_possessive_agreements()
        self._register_noun_cases()
        self._register_noun_to_noun_derivations()
        self._register_noun_to_verb_derivations()
        self._register_noun_to_adjective_derivations()

    def _register_verb_suffixes(self):
        self._register_verb_agreements()
        self._register_verb_from_other_positions_agreements()
        self._register_verb_polarisations()
        self._register_verb_tenses()
        self._register_modal_verbs()
        self._register_verb_to_verb_derivations()
        self._register_verb_to_noun_derivations()
        self._register_verb_to_adverb_derivations()
        self._register_verb_to_adjective_derivations()

    def _register_adjective_suffixes(self):
        self._register_adjective_to_adverb_derivations()
        self._register_adjective_to_noun_derivations()
        self._register_adjective_to_verb_derivations()
        self._register_adjective_possessions()

    def _register_pronoun_suffixes(self):
        self._register_pronoun_agreements()
        self._register_pronoun_possessions()
        self._register_pronoun_cases()
        self._register_pronoun_to_adjective_suffixes()


    def _register_noun_agreements(self):
        self.NOUN_ROOT.add_out_suffix(self.A3Sg_Noun, self.NOUN_WITH_AGREEMENT)
        self.A3Sg_Noun.add_suffix_form("")

        self.NOUN_ROOT.add_out_suffix(self.A3Pl_Noun, self.NOUN_WITH_AGREEMENT)
        self.A3Pl_Noun.add_suffix_form("lAr")

    def _register_possessive_agreements(self):
        self.NOUN_WITH_AGREEMENT.add_out_suffix(self.Pnon_Noun, self.NOUN_WITH_POSSESSION)
        self.Pnon_Noun.add_suffix_form("")

        self.NOUN_WITH_AGREEMENT.add_out_suffix(self.P1Sg_Noun, self.NOUN_WITH_POSSESSION)
        self.P1Sg_Noun.add_suffix_form("+Im")

        self.NOUN_WITH_AGREEMENT.add_out_suffix(self.P2Sg_Noun, self.NOUN_WITH_POSSESSION)
        self.P2Sg_Noun.add_suffix_form("+In")

        self.NOUN_WITH_AGREEMENT.add_out_suffix(self.P3Sg_Noun, self.NOUN_WITH_POSSESSION)
        self.P3Sg_Noun.add_suffix_form("+sI")

        self.NOUN_WITH_AGREEMENT.add_out_suffix(self.P1Pl_Noun, self.NOUN_WITH_POSSESSION)
        self.P1Pl_Noun.add_suffix_form("+ImIz")

        self.NOUN_WITH_AGREEMENT.add_out_suffix(self.P2Pl_Noun, self.NOUN_WITH_POSSESSION)
        self.P2Pl_Noun.add_suffix_form("+InIz")

        self.NOUN_WITH_AGREEMENT.add_out_suffix(self.P3Pl_Noun, self.NOUN_WITH_POSSESSION)
        self.P3Pl_Noun.add_suffix_form("lArI")
        self.P3Pl_Noun.add_suffix_form("I", comes_after(self.A3Pl_Noun))

    def _register_noun_cases(self):
        comes_after_P3 = comes_after(self.P3Sg_Noun) | comes_after(self.P3Pl_Noun)
        doesnt_come_after_P3 = ~comes_after_P3

        self.NOUN_WITH_POSSESSION.add_out_suffix(self.Nom_Noun, self.NOUN_WITH_CASE)
        self.Nom_Noun.add_suffix_form("")

        self.NOUN_WITH_POSSESSION.add_out_suffix(self.Nom_Noun_Deriv, self.NOUN_NOM_DERIV)
        self.Nom_Noun_Deriv.add_suffix_form("", comes_after(self.Pnon_Noun))

        self.NOUN_WITH_POSSESSION.add_out_suffix(self.Acc_Noun, self.NOUN_WITH_CASE)
        self.Acc_Noun.add_suffix_form(u"+yI", doesnt_come_after_P3)
        self.Acc_Noun.add_suffix_form(u"nI", comes_after_P3)

        self.NOUN_WITH_POSSESSION.add_out_suffix(self.Dat_Noun, self.NOUN_WITH_CASE)
        self.Dat_Noun.add_suffix_form(u"+yA", doesnt_come_after_P3)
        self.Dat_Noun.add_suffix_form(u"nA", comes_after_P3)

        self.NOUN_WITH_POSSESSION.add_out_suffix(self.Loc_Noun, self.NOUN_WITH_CASE)
        self.Loc_Noun.add_suffix_form(u"dA", doesnt_come_after_P3 & doesnt_come_after_derivation(self.Inf, "mAk"))
        self.Loc_Noun.add_suffix_form(u"ndA")

        self.NOUN_WITH_POSSESSION.add_out_suffix(self.Abl_Noun, self.NOUN_WITH_CASE)
        self.Abl_Noun.add_suffix_form(u"dAn", doesnt_come_after_P3)
        self.Abl_Noun.add_suffix_form(u"ndAn")

        self.NOUN_WITH_POSSESSION.add_out_suffix(self.Gen_Noun, self.NOUN_WITH_CASE)
        self.Gen_Noun.add_suffix_form(u"+nIn")

        self.NOUN_WITH_POSSESSION.add_out_suffix(self.Ins_Noun, self.NOUN_WITH_CASE)
        self.Ins_Noun.add_suffix_form(u"+ylA")

    def _register_noun_to_noun_derivations(self):
        self.NOUN_NOM_DERIV.add_out_suffix(self.Agt_Noun, self.NOUN_ROOT)
        self.Agt_Noun.add_suffix_form(u"cI")

        self.NOUN_NOM_DERIV.add_out_suffix(self.Dim, self.NOUN_ROOT)
        self.Dim.add_suffix_form(u"cIk")

    def _register_noun_to_verb_derivations(self):
        self.NOUN_NOM_DERIV.add_out_suffix(self.Acquire, self.VERB_ROOT)
        self.Acquire.add_suffix_form(u"lAn")

    def _register_noun_to_adjective_derivations(self):
        self.NOUN_NOM_DERIV.add_out_suffix(self.With, self.ADJECTIVE_ROOT)
        self.With.add_suffix_form(u"lI")

        self.NOUN_NOM_DERIV.add_out_suffix(self.Without, self.ADJECTIVE_ROOT)
        self.Without.add_suffix_form(u"sIz")

        self.NOUN_DERIV_WITH_CASE.add_out_suffix(self.Rel, self.ADJECTIVE_ROOT)
        self.Rel.add_suffix_form(u"ki")

    def _register_verb_polarisations(self):
        self.VERB_ROOT.add_out_suffix(self.Negative, self.VERB_WITH_POLARITY)
        self.Negative.add_suffix_form(u"m", postcondition=doesnt(followed_by_suffix(that_goes_to(State.DERIV))))
        self.Negative.add_suffix_form(u"mA")

        self.VERB_ROOT.add_out_suffix(self.Positive, self.VERB_WITH_POLARITY)
        self.Positive.add_suffix_form("")

    def _register_verb_tenses(self):
        self.Aorist.add_suffix_form(u"+Ir", requires_root_attribute(RootAttribute.Aorist_I))
        self.Aorist.add_suffix_form(u"+Ar")
        self.Aorist.add_suffix_form(u"z", comes_after(self.Negative))    # gel-me-z or gel-me-z-sin
        self.Aorist.add_suffix_form(u"", comes_after(self.Negative), followed_by(self.A1Sg_Verb) or followed_by(self.A1Pl_Verb))     # gel-me-m or gel-me-yiz

        self.Progressive.add_suffix_form(u"Iyor")
        self.Progressive.add_suffix_form(u"mAktA")

        self.Future.add_suffix_form(u"+yAcAk")

        self.Narr.add_suffix_form(u"mIş")
        self.Narr.add_suffix_form(u"ymIş")

        self.Past.add_suffix_form(u"dI")
        self.Past.add_suffix_form(u"ydI")

        self.Cond.add_suffix_form(u"+ysA")

        self.Imp.add_suffix_form(u"", postcondition=followed_by(self.A2Sg_Verb) | followed_by(self.A3Sg_Verb) | followed_by(self.A2Pl_Verb) | followed_by(self.A3Pl_Verb))
        self.Imp.add_suffix_form(u"sAnA", postcondition=followed_by(self.A2Sg_Verb))
        self.Imp.add_suffix_form(u"sAnIzA", postcondition=followed_by(self.A2Pl_Verb))

        self.Pres.add_suffix_form(u"")

        self.VERB_WITH_POLARITY.add_out_suffix(self.Aorist, self.VERB_WITH_TENSE)
        self.VERB_WITH_POLARITY.add_out_suffix(self.Progressive, self.VERB_WITH_TENSE)
        self.VERB_WITH_POLARITY.add_out_suffix(self.Future, self.VERB_WITH_TENSE)
        self.VERB_WITH_POLARITY.add_out_suffix(self.Narr, self.VERB_WITH_TENSE)
        self.VERB_WITH_POLARITY.add_out_suffix(self.Past, self.VERB_WITH_TENSE)
        self.VERB_WITH_POLARITY.add_out_suffix(self.Cond, self.VERB_WITH_TENSE)
        self.VERB_WITH_POLARITY.add_out_suffix(self.Imp, self.VERB_WITH_TENSE)

        self.VERB_WITH_TENSE.add_out_suffix(self.Cond, self.VERB_WITH_TENSE)
        self.VERB_WITH_TENSE.add_out_suffix(self.Narr, self.VERB_WITH_TENSE)
        self.VERB_WITH_TENSE.add_out_suffix(self.Past, self.VERB_WITH_TENSE)

        self.VERB_FROM_OTHER_POS.add_out_suffix(self.Cond, self.VERB_FROM_OTHER_POS_WITH_TENSE)
        self.VERB_FROM_OTHER_POS.add_out_suffix(self.Narr, self.VERB_FROM_OTHER_POS_WITH_TENSE)
        self.VERB_FROM_OTHER_POS.add_out_suffix(self.Past, self.VERB_FROM_OTHER_POS_WITH_TENSE)
        self.VERB_FROM_OTHER_POS.add_out_suffix(self.Pres, self.VERB_FROM_OTHER_POS_WITH_TENSE)

    def _register_verb_agreements(self):
        comes_after_imperative = comes_after(self.Imp)
        doesnt_come_after_imperative = doesnt(comes_after_imperative)
        comes_after_empty_imperative = comes_after(self.Imp, u"")
        doesnt_come_after_empty_imperative = doesnt(comes_after_empty_imperative)

        self.VERB_WITH_TENSE.add_out_suffix(self.A1Sg_Verb, self.VERB_TERMINAL)
        self.A1Sg_Verb.add_suffix_form("+Im")
        self.A1Sg_Verb.add_suffix_form("yIm")   #"yap-makta-yım", gel-meli-yim

        self.VERB_WITH_TENSE.add_out_suffix(self.A2Sg_Verb, self.VERB_TERMINAL)
        self.A2Sg_Verb.add_suffix_form("n", doesnt_come_after_imperative)
        self.A2Sg_Verb.add_suffix_form("sIn", doesnt_come_after_imperative)
        self.A2Sg_Verb.add_suffix_form("", comes_after_imperative)

        self.VERB_WITH_TENSE.add_out_suffix(self.A3Sg_Verb, self.VERB_TERMINAL)
        self.A3Sg_Verb.add_suffix_form("", doesnt_come_after_imperative)
        self.A3Sg_Verb.add_suffix_form("sIn", comes_after_imperative)

        self.VERB_WITH_TENSE.add_out_suffix(self.A1Pl_Verb, self.VERB_TERMINAL)
        self.A1Pl_Verb.add_suffix_form("+Iz", doesnt_come_after(self.Opt))
        self.A1Pl_Verb.add_suffix_form("k",   doesnt_come_after(self.Opt))     # only for "gel-di-k"
        self.A1Pl_Verb.add_suffix_form("yIz", doesnt_come_after(self.Opt))   # "yap-makta-yız" OR "gel-me-yiz"
        self.A1Pl_Verb.add_suffix_form("lIm", comes_after(self.Opt))     # only for "gel-e-lim"

        self.VERB_WITH_TENSE.add_out_suffix(self.A2Pl_Verb, self.VERB_TERMINAL)
        self.A2Pl_Verb.add_suffix_form("", comes_after_imperative & doesnt_come_after_empty_imperative)
        self.A2Pl_Verb.add_suffix_form("sInIz", doesnt_come_after_imperative)
        self.A2Pl_Verb.add_suffix_form("nIz", doesnt_come_after_imperative)
        self.A2Pl_Verb.add_suffix_form("+yIn", comes_after_empty_imperative)
        self.A2Pl_Verb.add_suffix_form("+yInIz", comes_after_empty_imperative)

        self.VERB_WITH_TENSE.add_out_suffix(self.A3Pl_Verb, self.VERB_TERMINAL)
        self.A3Pl_Verb.add_suffix_form("lAr", doesnt_come_after_imperative)
        self.A3Pl_Verb.add_suffix_form("sInlAr", comes_after_imperative)

    def _register_verb_from_other_positions_agreements(self):
        comes_after_cond_or_past = comes_after(self.Cond) | comes_after(self.Past)

        self.VERB_FROM_OTHER_POS_WITH_TENSE.add_out_suffix(self.A1Sg_Verb_From_Other_Pos, self.VERB_TERMINAL)
        self.A1Sg_Verb_From_Other_Pos.add_suffix_form("+yIm")                          # (ben) elma-yim, (ben) armud-um, elma-ymis-im
        self.A1Sg_Verb_From_Other_Pos.add_suffix_form("m", comes_after_cond_or_past)   # elma-ydi-m, elma-ysa-m

        self.VERB_FROM_OTHER_POS_WITH_TENSE.add_out_suffix(self.A2Sg_Verb_From_Other_Pos, self.VERB_TERMINAL)
        self.A2Sg_Verb_From_Other_Pos.add_suffix_form("sIn")                           # (sen) elma-sin, (sen) armutsun, elma-ymis-sin
        self.A2Sg_Verb_From_Other_Pos.add_suffix_form("n", comes_after_cond_or_past)   # elma-ydi-n, elma-ysa-n

        self.VERB_FROM_OTHER_POS_WITH_TENSE.add_out_suffix(self.A3Sg_Verb_From_Other_Pos, self.VERB_TERMINAL)
        self.A3Sg_Verb_From_Other_Pos.add_suffix_form("")                              # (o) elma(dir), (o) armut(tur), elma-ymis, elma-ysa, elma-ydi

        self.VERB_FROM_OTHER_POS_WITH_TENSE.add_out_suffix(self.A1Pl_Verb_From_Other_Pos, self.VERB_TERMINAL)
        self.A1Pl_Verb_From_Other_Pos.add_suffix_form("+yIz")                          # (biz) elma-yiz, (biz) armud-uz, elma-ymis-iz
        self.A1Pl_Verb_From_Other_Pos.add_suffix_form("k", comes_after_cond_or_past)   # elma-ydi-k, elma-ysa-k

        self.VERB_FROM_OTHER_POS_WITH_TENSE.add_out_suffix(self.A2Pl_Verb_From_Other_Pos, self.VERB_TERMINAL)
        self.A2Pl_Verb_From_Other_Pos.add_suffix_form("sInIz")                         # (siz) elma-siniz, (siz) armut-sunuz, elma-ymis-siniz
        self.A2Pl_Verb_From_Other_Pos.add_suffix_form("nIz", comes_after_cond_or_past) # elma-ydi-niz, elma-ysa-niz

        self.VERB_FROM_OTHER_POS_WITH_TENSE.add_out_suffix(self.A3Pl_Verb_From_Other_Pos, self.VERB_TERMINAL)
        self.A3Pl_Verb_From_Other_Pos.add_suffix_form("lAr")    # (onlar) elma-lar(dir), (onlar) armut-lar(dir), elma-ymis-lar, elma-ydi-lar, elma-ysa-lar

    def _register_modal_verbs(self):
        followed_by_modal_followers = followed_by(self.Past) | followed_by(self.Narr) | followed_by_one_from_group(self.Verb_Agreements_Group)

        self.VERB_WITH_POLARITY.add_out_suffix(self.Neces, self.VERB_WITH_TENSE)
        self.Neces.add_suffix_form(u"mAlI!")

        self.VERB_WITH_POLARITY.add_out_suffix(self.Opt, self.VERB_WITH_TENSE)
        self.Opt.add_suffix_form(u"Ay")
        self.Opt.add_suffix_form(u"A", doesnt_come_after(self.Negative), followed_by_modal_followers)
        self.Opt.add_suffix_form(u"yAy")
        self.Opt.add_suffix_form(u"yA", postcondition=followed_by_modal_followers)

    def _register_verb_to_verb_derivations(self):
        self.VERB_PLAIN_DERIV.add_out_suffix(self.Able, self.VERB_ROOT)
        self.Able.add_suffix_form(u"+yAbil", postcondition=doesnt(followed_by(self.Negative)))
        self.Able.add_suffix_form(u"+yA", postcondition=followed_by(self.Negative))

        self.VERB_POLARITY_DERIV.add_out_suffix(self.Hastily, self.VERB_ROOT)
        self.Hastily.add_suffix_form(u"+yIver")

        self.VERB_PLAIN_DERIV.add_out_suffix(self.Pass, self.VERB_ROOT)
        self.Pass.add_suffix_form(u"+In")
        self.Pass.add_suffix_form(u"+nIl")
        self.Pass.add_suffix_form(u"+InIl")

        self.VERB_PLAIN_DERIV.add_out_suffix(self.Recip, self.VERB_ROOT)
        self.Recip.add_suffix_form(u"+Iş", post_derivation_condition=doesnt(followed_by_derivation(self.Caus)))

        self.VERB_PLAIN_DERIV.add_out_suffix(self.Caus, self.VERB_ROOT)
        self.Caus.add_suffix_form(u"t",  requires_root_attribute(RootAttribute.Causative_t) & doesnt_come_after_derivation(self.Caus, "t") & doesnt_come_after_derivation(self.Caus, "It"))
        self.Caus.add_suffix_form(u"Ir", requires_root_attribute(RootAttribute.Causative_Ir) & doesnt_come_after_derivation(self.Able))
        self.Caus.add_suffix_form(u"It", requires_root_attribute(RootAttribute.Causative_It) & doesnt_come_after_derivation(self.Able))
        self.Caus.add_suffix_form(u"Ar", requires_root_attribute(RootAttribute.Causative_Ar) & doesnt_come_after_derivation(self.Able))
        self.Caus.add_suffix_form(u"dIr", requires_root_attribute(RootAttribute.Causative_dIr))

    def _register_verb_to_noun_derivations(self):
        self.VERB_POLARITY_DERIV.add_out_suffix(self.Inf, self.NOUN_ROOT)
        self.Inf.add_suffix_form(u"mAk")
        self.Inf.add_suffix_form(u"mA")
        self.Inf.add_suffix_form(u"+yIş")

        self.VERB_POLARITY_DERIV.add_out_suffix(self.PastPart_Noun, self.NOUN_ROOT)
        self.PastPart_Noun.add_suffix_form(u"dIk")

        self.VERB_POLARITY_DERIV.add_out_suffix(self.FutPart_Noun, self.NOUN_ROOT)
        self.FutPart_Noun.add_suffix_form(u'+yAcAk')

    def _register_verb_to_adverb_derivations(self):
        self.VERB_POLARITY_DERIV.add_out_suffix(self.AfterDoingSo, self.ADVERB_ROOT)
        self.AfterDoingSo.add_suffix_form(u"+yIp")

        self.VERB_POLARITY_DERIV.add_out_suffix(self.AsLongAs, self.ADVERB_ROOT)
        self.AsLongAs.add_suffix_form(u"dIkçA")

        self.VERB_POLARITY_DERIV.add_out_suffix(self.ByDoingSo, self.ADVERB_ROOT)
        self.ByDoingSo.add_suffix_form(u"+yArAk")

        self.VERB_TENSE_DERIV.add_out_suffix(self.While, self.ADVERB_ROOT)
        self.While.add_suffix_form(u"ken")

        self.VERB_TENSE_DERIV.add_out_suffix(self.AsIf, self.ADVERB_ROOT)
        self.AsIf.add_suffix_form(u"cAsInA")

    def _register_verb_to_adjective_derivations(self):
        self.VERB_POLARITY_DERIV.add_out_suffix(self.PresPart, self.ADJECTIVE_ROOT)
        self.PresPart.add_suffix_form(u'An')

        self.VERB_POLARITY_DERIV.add_out_suffix(self.PastPart_Adj, self.ADJECTIVE_PART_WITHOUT_POSSESSION)
        self.PastPart_Adj.add_suffix_form(u'dIk')

        self.VERB_POLARITY_DERIV.add_out_suffix(self.FutPart_Adj, self.ADJECTIVE_PART_WITHOUT_POSSESSION)
        self.FutPart_Adj.add_suffix_form(u'+yAcAk')

        self.VERB_POLARITY_DERIV.add_out_suffix(self.Agt_Adj, self.ADJECTIVE_ROOT)
        self.Agt_Adj.add_suffix_form(u"+yIcI")


        self.VERB_WITH_POLARITY.add_out_suffix(self.Aorist_to_Adj, self.VERB_TENSE_ADJ_DERIV)
        self.Aorist_to_Adj.add_suffix_form(u"+Ir", requires_root_attribute(RootAttribute.Aorist_I))
        self.Aorist_to_Adj.add_suffix_form(u"+Ar")
        self.Aorist_to_Adj.add_suffix_form(u"z", comes_after(self.Negative))    # gel-me-z

        self.VERB_WITH_POLARITY.add_out_suffix(self.Narr_to_Adj, self.VERB_TENSE_ADJ_DERIV)
        self.Narr_to_Adj.add_suffix_form(u"mIş")
        self.Narr_to_Adj.add_suffix_form(u"ymIş")

    def _register_adjective_to_adverb_derivations(self):
        self.ADJECTIVE_DERIV.add_out_suffix(self.Ly, self.ADVERB_ROOT)
        self.Ly.add_suffix_form(u"cA")

    def _register_adjective_to_noun_derivations(self):
        self.ADJECTIVE_DERIV.add_out_suffix(self.Ness, self.NOUN_ROOT)
        self.Ness.add_suffix_form(u"lIk")

    def _register_adjective_to_verb_derivations(self):
        self.ADJECTIVE_DERIV.add_out_suffix(self.Become, self.VERB_ROOT)
        self.Become.add_suffix_form(u"lAş")

    def _register_adjective_possessions(self):
        self.ADJECTIVE_PART_WITHOUT_POSSESSION.add_out_suffix(self.Pnon_Adj, self.ADJECTIVE_TERMINAL)
        self.Pnon_Adj.add_suffix_form("")

        self.ADJECTIVE_PART_WITHOUT_POSSESSION.add_out_suffix(self.P1Sg_Adj, self.ADJECTIVE_TERMINAL)
        self.P1Sg_Adj.add_suffix_form("+Im")

        self.ADJECTIVE_PART_WITHOUT_POSSESSION.add_out_suffix(self.P2Sg_Adj, self.ADJECTIVE_TERMINAL)
        self.P2Sg_Adj.add_suffix_form("+In")

        self.ADJECTIVE_PART_WITHOUT_POSSESSION.add_out_suffix(self.P3Sg_Adj, self.ADJECTIVE_TERMINAL)
        self.P3Sg_Adj.add_suffix_form("+sI")

        self.ADJECTIVE_PART_WITHOUT_POSSESSION.add_out_suffix(self.P1Pl_Adj, self.ADJECTIVE_TERMINAL)
        self.P1Pl_Adj.add_suffix_form("+ImIz")

        self.ADJECTIVE_PART_WITHOUT_POSSESSION.add_out_suffix(self.P2Pl_Adj, self.ADJECTIVE_TERMINAL)
        self.P2Pl_Adj.add_suffix_form("+InIz")

        self.ADJECTIVE_PART_WITHOUT_POSSESSION.add_out_suffix(self.P3Pl_Adj, self.ADJECTIVE_TERMINAL)
        self.P3Pl_Adj.add_suffix_form("lArI")

    def _register_pronoun_agreements(self):
        self.PRONOUN_ROOT.add_out_suffix(self.A1Sg_Pron, self.PRONOUN_WITH_AGREEMENT)
        #A1Sg_Pron forms are predefined, 'ben' and 'kendi'

        self.PRONOUN_ROOT.add_out_suffix(self.A2Sg_Pron, self.PRONOUN_WITH_AGREEMENT)
        #A2Sg_Pron forms are predefined, 'sen' and 'kendi'

        self.PRONOUN_ROOT.add_out_suffix(self.A3Sg_Pron, self.PRONOUN_WITH_AGREEMENT)
        self.A3Sg_Pron.add_suffix_form("")
        #A3Sg_Pron forms for 'o', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_ROOT.add_out_suffix(self.A1Pl_Pron, self.PRONOUN_WITH_AGREEMENT)
        #A1Pl_Pron forms are predefined, 'biz' and 'kendi'

        self.PRONOUN_ROOT.add_out_suffix(self.A2Pl_Pron, self.PRONOUN_WITH_AGREEMENT)
        #A2Pl_Pron forms are predefined, 'siz' and 'kendi'

        self.PRONOUN_ROOT.add_out_suffix(self.A3Pl_Pron, self.PRONOUN_WITH_AGREEMENT)
        self.A3Pl_Pron.add_suffix_form("lAr")
        #A3Pl_Pron forms for 'onlar', 'bunlar', 'sunlar', 'kendileri' are predefined


    def _register_pronoun_possessions(self):
        self.PRONOUN_WITH_AGREEMENT.add_out_suffix(self.Pnon_Pron, self.PRONOUN_WITH_POSSESSION)
        self.Pnon_Pron.add_suffix_form("")
        #Pnon_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_AGREEMENT.add_out_suffix(self.P1Sg_Pron, self.PRONOUN_WITH_POSSESSION)
        self.P1Sg_Pron.add_suffix_form("+Im")
        #P1Sg_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_AGREEMENT.add_out_suffix(self.P2Sg_Pron, self.PRONOUN_WITH_POSSESSION)
        self.P2Sg_Pron.add_suffix_form("+In")
        #P2Sg_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_AGREEMENT.add_out_suffix(self.P3Sg_Pron, self.PRONOUN_WITH_POSSESSION)
        self.P3Sg_Pron.add_suffix_form("+sI")
        #P3Sg_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_AGREEMENT.add_out_suffix(self.P1Pl_Pron, self.PRONOUN_WITH_POSSESSION)
        self.P1Pl_Pron.add_suffix_form("+ImIz")
        #P1Pl_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_AGREEMENT.add_out_suffix(self.P2Pl_Pron, self.PRONOUN_WITH_POSSESSION)
        self.P2Pl_Pron.add_suffix_form("+InIz")
        #P2Pl_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_AGREEMENT.add_out_suffix(self.P3Pl_Pron, self.PRONOUN_WITH_POSSESSION)
        self.P3Pl_Pron.add_suffix_form("lArI")
        self.P3Pl_Pron.add_suffix_form("I", comes_after(self.A3Pl_Pron))
        #P3Pl_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

    def _register_pronoun_cases(self):
        self.PRONOUN_WITH_POSSESSION.add_out_suffix(self.Nom_Pron, self.PRONOUN_WITH_CASE)
        self.Nom_Pron.add_suffix_form("")

        self.PRONOUN_WITH_POSSESSION.add_out_suffix(self.Nom_Pron_Deriv, self.PRONOUN_NOM_DERIV)
        self.Nom_Pron_Deriv.add_suffix_form("", comes_after(self.Pnon_Pron))

        self.PRONOUN_WITH_POSSESSION.add_out_suffix(self.Acc_Pron, self.PRONOUN_WITH_CASE)
        self.Acc_Pron.add_suffix_form(u"+yI")
        #Acc_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_POSSESSION.add_out_suffix(self.Dat_Pron, self.PRONOUN_WITH_CASE)
        self.Dat_Pron.add_suffix_form(u"+yA")
        #Dat_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_POSSESSION.add_out_suffix(self.Loc_Pron, self.PRONOUN_WITH_CASE)
        self.Loc_Pron.add_suffix_form(u"dA")
        #Loc_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_POSSESSION.add_out_suffix(self.Abl_Pron, self.PRONOUN_WITH_CASE)
        self.Abl_Pron.add_suffix_form(u"dAn")
        #Abl_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_POSSESSION.add_out_suffix(self.Gen_Pron, self.PRONOUN_WITH_CASE)
        self.Gen_Pron.add_suffix_form(u"+nIn")
        #Gen_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

        self.PRONOUN_WITH_POSSESSION.add_out_suffix(self.Ins_Pron, self.PRONOUN_WITH_CASE)
        self.Ins_Pron.add_suffix_form(u"+ylA")
        #Ins_Pron forms for 'ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'su', 'kendi' are predefined

    def _register_pronoun_to_adjective_suffixes(self):
        applies_to_bu_su_o = applies_to_stem('o') | applies_to_stem('bu') | applies_to_stem(u'şu')

        comes_after_A3Sg_pnon = comes_after(self.A3Sg_Pron) & comes_after(self.Pnon_Pron)

        comes_after_bu_su_o_pnon = comes_after_A3Sg_pnon & applies_to_bu_su_o

        self.PRONOUN_NOM_DERIV.add_out_suffix(self.Without_Pron, self.ADJECTIVE_ROOT)
        self.Without_Pron.add_suffix_form(u"sIz", doesnt(comes_after_bu_su_o_pnon))  # ben-siz, onlar-siz
        self.Without_Pron.add_suffix_form(u"nsuz", comes_after_bu_su_o_pnon)         # o-nsuz, bu-nsuz, su-nsuz